"""
OAuth Provider Configuration System
Supports multiple OAuth providers with a flexible architecture
"""
import os
from typing import Dict, Any, Optional
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.discord import DiscordOAuth2
from httpx_oauth.clients.microsoft import MicrosoftGraphOAuth2
from .google_oauth_handler import GoogleOAuthHandler
from dotenv import load_dotenv
    
    
load_dotenv()


class OAuthProviderConfig:
    """Configuration for OAuth providers"""
    
    def __init__(self, name: str, client_id: str, client_secret: str, redirect_uri: str):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri


class OAuthManager:
    """Manages OAuth providers and their configurations"""
    
    def __init__(self):
        self.providers: Dict[str, Any] = {}
        self._setup_providers()
    
    def _setup_providers(self):
        """Setup available OAuth providers based on environment variables"""
        
        # Google OAuth
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/oauth/google/callback")
        
        if google_client_id and google_client_secret:
            self.providers["google"] = {
                "client": GoogleOAuthHandler(google_client_id, google_client_secret),
                "config": OAuthProviderConfig("google", google_client_id, google_client_secret, google_redirect_uri),
                "scopes": ["openid", "email", "profile"]
            }
        
        # GitHub OAuth (for future use)
        github_client_id = os.getenv("GITHUB_CLIENT_ID")
        github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        github_redirect_uri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/api/v1/auth/oauth/github/callback")
        
        if github_client_id and github_client_secret:
            self.providers["github"] = {
                "client": GitHubOAuth2(github_client_id, github_client_secret),
                "config": OAuthProviderConfig("github", github_client_id, github_client_secret, github_redirect_uri),
                "scopes": ["user:email"]
            }
        
        # Discord OAuth (for future use)
        discord_client_id = os.getenv("DISCORD_CLIENT_ID")
        discord_client_secret = os.getenv("DISCORD_CLIENT_SECRET")
        discord_redirect_uri = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:8000/api/v1/auth/oauth/discord/callback")
        
        if discord_client_id and discord_client_secret:
            self.providers["discord"] = {
                "client": DiscordOAuth2(discord_client_id, discord_client_secret),
                "config": OAuthProviderConfig("discord", discord_client_id, discord_client_secret, discord_redirect_uri),
                "scopes": ["identify", "email"]
            }
        
        # Microsoft OAuth (for future use)
        microsoft_client_id = os.getenv("MICROSOFT_CLIENT_ID")
        microsoft_client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")
        microsoft_redirect_uri = os.getenv("MICROSOFT_REDIRECT_URI", "http://localhost:8000/api/v1/auth/oauth/microsoft/callback")
        
        if microsoft_client_id and microsoft_client_secret:
            self.providers["microsoft"] = {
                "client": MicrosoftGraphOAuth2(microsoft_client_id, microsoft_client_secret),
                "config": OAuthProviderConfig("microsoft", microsoft_client_id, microsoft_client_secret, microsoft_redirect_uri),
                "scopes": ["openid", "email", "profile"]
            }
    
    def get_provider(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """Get OAuth provider configuration by name"""
        return self.providers.get(provider_name)
    
    def get_available_providers(self) -> list[str]:
        """Get list of available OAuth providers"""
        return list(self.providers.keys())
    
    def is_provider_available(self, provider_name: str) -> bool:
        """Check if a provider is configured and available"""
        return provider_name in self.providers

    def log_available_providers(self):
        """Log available OAuth providers"""
        print("Available OAuth providers:")
        for provider in self.providers:
            print(f"- {provider}")


# Global OAuth manager instance
oauth_manager = OAuthManager()

oauth_manager.log_available_providers()