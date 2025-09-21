"""
API Key Management Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
import models
import schemas
from core.database import get_db
from core.auth import current_active_user
from core.security import generate_api_key

router = APIRouter()

@router.post("/api-keys", response_model=schemas.ApiKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    api_key_data: schemas.ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Create a new API key for the authenticated user"""
    # Generate a unique API key
    api_key = generate_api_key()
    
    # Create the API key record
    db_api_key = models.ApiKey(
        key=api_key,
        name=api_key_data.name,
        description=api_key_data.description,
        expires_at=api_key_data.expires_at,
        user_id=user.id
    )
    
    db.add(db_api_key)
    await db.commit()
    await db.refresh(db_api_key)
    
    return db_api_key

@router.get("/api-keys", response_model=List[schemas.ApiKeyRead])
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """List all API keys for the authenticated user"""
    result = await db.execute(
        select(models.ApiKey)
        .where(models.ApiKey.user_id == user.id)
        .order_by(models.ApiKey.created_at.desc())
    )
    api_keys = result.scalars().all()
    
    # Return API keys without the full key for security
    return [
        schemas.ApiKeyRead(
            id=key.id,
            key=f"{key.key[:8]}...{key.key[-4:]}" if key.key else "",  # Mask the key
            name=key.name,
            description=key.description,
            is_active=key.is_active,
            last_used=key.last_used,
            created_at=key.created_at,
            expires_at=key.expires_at,
            user_id=key.user_id
        )
        for key in api_keys
    ]

@router.get("/api-keys/{key_id}", response_model=schemas.ApiKeyRead)
async def get_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Get a specific API key by ID"""
    result = await db.execute(
        select(models.ApiKey)
        .where(models.ApiKey.id == key_id)
        .where(models.ApiKey.user_id == user.id)
    )
    api_key = result.scalars().first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return schemas.ApiKeyRead(
        id=api_key.id,
        key=f"{api_key.key[:8]}...{api_key.key[-4:]}" if api_key.key else "",  # Mask the key
        name=api_key.name,
        description=api_key.description,
        is_active=api_key.is_active,
        last_used=api_key.last_used,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at,
        user_id=api_key.user_id
    )

@router.put("/api-keys/{key_id}", response_model=schemas.ApiKeyRead)
async def update_api_key(
    key_id: int,
    api_key_update: schemas.ApiKeyUpdate,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Update an API key"""
    result = await db.execute(
        select(models.ApiKey)
        .where(models.ApiKey.id == key_id)
        .where(models.ApiKey.user_id == user.id)
    )
    api_key = result.scalars().first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    # Update fields if provided
    if api_key_update.name is not None:
        api_key.name = api_key_update.name
    if api_key_update.description is not None:
        api_key.description = api_key_update.description
    if api_key_update.is_active is not None:
        api_key.is_active = api_key_update.is_active
    if api_key_update.expires_at is not None:
        api_key.expires_at = api_key_update.expires_at
    
    await db.commit()
    await db.refresh(api_key)
    
    return schemas.ApiKeyRead(
        id=api_key.id,
        key=f"{api_key.key[:8]}...{api_key.key[-4:]}" if api_key.key else "",  # Mask the key
        name=api_key.name,
        description=api_key.description,
        is_active=api_key.is_active,
        last_used=api_key.last_used,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at,
        user_id=api_key.user_id
    )

@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(current_active_user)
):
    """Delete an API key"""
    result = await db.execute(
        select(models.ApiKey)
        .where(models.ApiKey.id == key_id)
        .where(models.ApiKey.user_id == user.id)
    )
    api_key = result.scalars().first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    await db.delete(api_key)
    await db.commit()
    
    return None
