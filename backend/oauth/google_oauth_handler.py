"""
Custom Google OAuth handler to avoid People API issues
"""
import httpx
from typing import Optional, Dict, Any


class GoogleOAuthHandler:
    """Custom Google OAuth handler that uses userinfo endpoint instead of People API"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    async def get_access_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
            }
            
            response = await client.post(self.token_url, data=data)
            response.raise_for_status()
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Google userinfo endpoint"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await client.get(self.userinfo_url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def get_authorization_url(self, redirect_uri: str, scopes: list = None) -> str:
        """Generate Google OAuth authorization URL"""
        if scopes is None:
            scopes = ["openid", "email", "profile"]
        
        scope_string = " ".join(scopes)
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope_string,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"


class GoogleUserInfo:
    """Simple user info class to match the expected interface"""
    
    def __init__(self, user_data: Dict[str, Any]):
        self.id = user_data.get("id", "")
        self.email = user_data.get("email", "")
        self.first_name = user_data.get("given_name", "")
        self.last_name = user_data.get("family_name", "")
        self.name = user_data.get("name", "")
        self.picture = user_data.get("picture", "")
    
    def __getattr__(self, name):
        """Handle any missing attributes gracefully"""
        return None
