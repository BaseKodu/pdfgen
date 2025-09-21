"""
OAuth package for handling third-party authentication providers
"""

from .oauth_config import oauth_manager
from .oauth_routes import router as oauth_router
from .google_oauth_handler import GoogleOAuthHandler, GoogleUserInfo

__all__ = [
    'oauth_manager',
    'oauth_router', 
    'GoogleOAuthHandler',
    'GoogleUserInfo'
]
