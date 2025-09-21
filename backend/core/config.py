"""
Application configuration
"""
import os
from typing import Optional

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/oauth/google/callback")

# API Keys
API_KEY_LENGTH = 32
API_KEY_EXPIRY_DAYS = 365  # Default expiry for API keys

# PDF Generation
PLAYWRIGHT_TIMEOUT = 30000  # 30 seconds
MAX_PDF_SIZE = 50 * 1024 * 1024  # 50MB
