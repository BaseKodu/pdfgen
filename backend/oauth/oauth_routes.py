"""
OAuth Routes for Google and other providers - Fixed version
"""
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models
import schemas
from database import get_db
from auth import current_active_user, get_user_manager
from .oauth_config import oauth_manager
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager
from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.discord import DiscordOAuth2
from httpx_oauth.clients.microsoft import MicrosoftGraphOAuth2
from .google_oauth_handler import GoogleOAuthHandler, GoogleUserInfo
import httpx_oauth
import os

# Create router
router = APIRouter()

# OAuth client mapping
OAUTH_CLIENTS = {
    "github": GitHubOAuth2,
    "discord": DiscordOAuth2,
    "microsoft": MicrosoftGraphOAuth2,
}


def get_oauth_client(provider_name: str):
    """Get OAuth client for a provider"""
    provider = oauth_manager.get_provider(provider_name)
    if not provider:
        raise HTTPException(status_code=404, detail=f"OAuth provider '{provider_name}' not configured")
    return provider["client"]


@router.get("/oauth/providers")
async def get_available_oauth_providers():
    """Get list of available OAuth providers"""
    return {
        "providers": oauth_manager.get_available_providers(),
        "available": len(oauth_manager.get_available_providers()) > 0
    }


@router.get("/oauth/{provider}/authorize")
async def oauth_authorize(
    provider: str,
    request: Request,
    scopes: List[str] = None
):
    """Get authorization URL for OAuth provider"""
    try:
        client = get_oauth_client(provider)
        provider_config = oauth_manager.get_provider(provider)
        
        # Use default scopes if none provided
        if not scopes:
            scopes = provider_config["scopes"]
        
        # Generate authorization URL
        if provider == "google":
            # Use custom Google handler
            authorization_url = await client.get_authorization_url(
                provider_config["config"].redirect_uri,
                scopes
            )
        else:
            # Use standard httpx-oauth for other providers
            authorization_url = await client.get_authorization_url(
                provider_config["config"].redirect_uri,
                scopes
            )
        
        return {"authorization_url": authorization_url}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate authorization URL: {str(e)}")


@router.get("/oauth/{provider}/callback")
async def oauth_callback(
    provider: str,
    request: Request,
    code: str,
    state: str = None,
    error: str = None,
    db: AsyncSession = Depends(get_db),
    user_manager: BaseUserManager = Depends(get_user_manager)
):
    """Handle OAuth callback"""
    if error:
        raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
    
    try:
        client = get_oauth_client(provider)
        provider_config = oauth_manager.get_provider(provider)
        
        # Exchange code for token
        token = await client.get_access_token(
            code,
            provider_config["config"].redirect_uri
        )
        
        # Get user info from OAuth provider
        if provider == "google":
            # Use custom Google handler
            user_data = await client.get_user_info(token["access_token"])
            user_info = GoogleUserInfo(user_data)
        else:
            # Use standard httpx-oauth for other providers
            user_info = await client.get_id_email(token["access_token"])
        
        if not user_info.email:
            raise HTTPException(
                status_code=400,
                detail="OAUTH_NOT_AVAILABLE_EMAIL"
            )
        
        # Check if user exists by email
        result = await db.execute(
            select(models.User).where(models.User.email == user_info.email)
        )
        user = result.scalars().first()
        
        if not user:
            # Create new user directly in database for OAuth users
            # This bypasses the password requirement for OAuth-only users
            user = models.User(
                email=user_info.email,
                hashed_password="",  # Empty password for OAuth users
                is_active=True,
                is_verified=True,  # Trust OAuth provider verification
                is_superuser=False,
                first_name=getattr(user_info, 'first_name', None),
                last_name=getattr(user_info, 'last_name', None),
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        # Check if OAuth account already exists
        result = await db.execute(
            select(models.OAuthAccount).where(
                models.OAuthAccount.user_id == user.id,
                models.OAuthAccount.oauth_name == provider.upper()
            )
        )
        oauth_account = result.scalars().first()
        
        if not oauth_account:
            # Create new OAuth account
            oauth_account = models.OAuthAccount(
                user_id=user.id,
                oauth_name=provider.upper(),
                access_token=token["access_token"],
                expires_at=token.get("expires_at"),
                account_id=user_info.id,
                account_email=user_info.email
            )
            db.add(oauth_account)
        else:
            # Update existing OAuth account
            oauth_account.access_token = token["access_token"]
            oauth_account.expires_at = token.get("expires_at")
            oauth_account.account_id = user_info.id
            oauth_account.account_email = user_info.email
        
        await db.commit()
        
        # Reload user with oauth_accounts relationship to avoid async context issues
        result = await db.execute(
            select(models.User)
            .options(selectinload(models.User.oauth_accounts))
            .where(models.User.id == user.id)
        )
        user_with_oauth = result.scalars().first()
        
        # Create JWT token for the user using the JWT strategy
        from auth import get_jwt_strategy
        jwt_strategy = get_jwt_strategy()
        token = await jwt_strategy.write_token(user_with_oauth)
        
        # Redirect to frontend with success and token
        frontend_url = "http://localhost:5173"  # Adjust this to your frontend URL
        redirect_url = f"{frontend_url}/auth/callback?success=true&token={token}"
        
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"OAuth callback failed: {str(e)}")


@router.get("/oauth/{provider}/associate/authorize")
async def oauth_associate_authorize(
    provider: str,
    request: Request,
    user: models.User = Depends(current_active_user),
    scopes: List[str] = None
):
    """Get authorization URL for associating OAuth account with existing user"""
    try:
        client = get_oauth_client(provider)
        provider_config = oauth_manager.get_provider(provider)
        
        # Use default scopes if none provided
        if not scopes:
            scopes = provider_config["scopes"]
        
        # Generate authorization URL with state to identify the user
        if provider == "google":
            # Use custom Google handler
            authorization_url = await client.get_authorization_url(
                provider_config["config"].redirect_uri,
                scopes
            )
        else:
            # Use standard httpx-oauth for other providers
            authorization_url = await client.get_authorization_url(
                provider_config["config"].redirect_uri,
                scopes,
                state=str(user.id)  # Include user ID in state
            )
        
        return {"authorization_url": authorization_url}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate association URL: {str(e)}")


@router.get("/oauth/{provider}/associate/callback")
async def oauth_associate_callback(
    provider: str,
    request: Request,
    code: str,
    state: str,
    user: models.User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Handle OAuth association callback"""
    try:
        client = get_oauth_client(provider)
        provider_config = oauth_manager.get_provider(provider)
        
        # Exchange code for token
        token = await client.get_access_token(
            code,
            provider_config["config"].redirect_uri
        )
        
        # Get user info from OAuth provider
        if provider == "google":
            # Use custom Google handler
            user_data = await client.get_user_info(token["access_token"])
            user_info = GoogleUserInfo(user_data)
        else:
            # Use standard httpx-oauth for other providers
            user_info = await client.get_id_email(token["access_token"])
        
        if not user_info.email:
            raise HTTPException(
                status_code=400,
                detail="OAUTH_NOT_AVAILABLE_EMAIL"
            )
        
        # Check if OAuth account already exists for this user
        result = await db.execute(
            select(models.OAuthAccount).where(
                models.OAuthAccount.user_id == user.id,
                models.OAuthAccount.oauth_name == provider.upper()
            )
        )
        oauth_account = result.scalars().first()
        
        if oauth_account:
            # Update existing OAuth account
            oauth_account.access_token = token["access_token"]
            oauth_account.expires_at = token.get("expires_at")
            oauth_account.account_id = user_info.id
            oauth_account.account_email = user_info.email
        else:
            # Create new OAuth account
            oauth_account = models.OAuthAccount(
                user_id=user.id,
                oauth_name=provider.upper(),
                access_token=token["access_token"],
                expires_at=token.get("expires_at"),
                account_id=user_info.id,
                account_email=user_info.email
            )
            db.add(oauth_account)
        
        await db.commit()
        await db.refresh(user)
        
        # Return updated user info
        return schemas.UserRead.model_validate(user)
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"OAuth association failed: {str(e)}")


@router.delete("/oauth/{provider}/disconnect")
async def oauth_disconnect(
    provider: str,
    user: models.User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Disconnect OAuth account from user"""
    try:
        # Find and delete OAuth account
        result = await db.execute(
            select(models.OAuthAccount).where(
                models.OAuthAccount.user_id == user.id,
                models.OAuthAccount.oauth_name == provider.upper()
            )
        )
        oauth_account = result.scalars().first()
        
        if not oauth_account:
            raise HTTPException(status_code=404, detail="OAuth account not found")
        
        await db.delete(oauth_account)
        await db.commit()
        
        return {"message": f"Successfully disconnected {provider} account"}
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to disconnect OAuth account: {str(e)}")
