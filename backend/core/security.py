"""
Security utilities and helpers
"""
import secrets
from typing import Optional
from datetime import datetime, timedelta
from .config import API_KEY_LENGTH, API_KEY_EXPIRY_DAYS

def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(API_KEY_LENGTH)

def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(length)

def is_token_expired(expires_at: Optional[datetime]) -> bool:
    """Check if a token is expired"""
    if expires_at is None:
        return False
    return datetime.utcnow() > expires_at

def get_default_expiry() -> datetime:
    """Get default expiry date for API keys"""
    return datetime.utcnow() + timedelta(days=API_KEY_EXPIRY_DAYS)
