"""
Shared API dependencies
"""
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

import models
from core.database import get_db

bearer_scheme = HTTPBearer()

async def get_user_from_api_key(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: AsyncSession = Depends(get_db)
) -> models.User:
    """
    Authenticates a user based on an API key provided in the Authorization header.
    Updates the last_used timestamp of the API key.
    """
    api_key_value = credentials.credentials

    result = await db.execute(
        select(models.ApiKey)
        .where(models.ApiKey.key == api_key_value, models.ApiKey.is_active == True)
    )
    api_key = result.scalars().first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if api_key.expires_at and api_key.expires_at < datetime.now():
        api_key.is_active = False
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last_used timestamp
    api_key.last_used = datetime.now()
    await db.commit()
    await db.refresh(api_key)

    # Fetch the associated user
    user_result = await db.execute(
        select(models.User).where(models.User.id == api_key.user_id)
    )
    user = user_result.scalars().first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Associated user is inactive or not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
