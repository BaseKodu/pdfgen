from pydantic import BaseModel, Json, field_validator
from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from fastapi_users import schemas
from enum import Enum


# API Key Schemas (defined early to avoid forward reference issues)
class ApiKeyBase(BaseModel):
    name: str
    description: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    @field_validator('expires_at', mode='before')
    @classmethod
    def parse_expires_at(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                return None
        return v

class ApiKeyCreate(ApiKeyBase):
    pass

class ApiKeyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None

class ApiKeyRead(ApiKeyBase):
    id: int
    key: str
    is_active: bool
    last_used: Optional[datetime] = None
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True

class ApiKeyResponse(ApiKeyRead):
    """Response schema that includes the full key (only shown once on creation)"""
    pass


# OAuth Account Schema
class OAuthAccountRead(BaseModel):
    id: int
    oauth_name: str
    account_id: str
    account_email: str
    expires_at: Optional[int] = None
    
    class Config:
        from_attributes = True

# FastAPI Users schemas
class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    oauth_accounts: Optional[List[OAuthAccountRead]] = None
    api_keys: Optional[List['ApiKeyRead']] = None

class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None



class TemplatingEngineEnum(str, Enum):
    JSX = "jsx"
    HTML = "html"
    VUE = "vue"

class TemplateBase(BaseModel):
    id: Optional[str] = None
    name: str
    engine: TemplatingEngineEnum = TemplatingEngineEnum.HTML
    content: str
    data: Optional[Dict[str, Any]] = None  # Optional JSON data

class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    content: Optional[str] = None
    data: Optional[dict] = None


class Template(TemplateBase):
    #user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PDFRequest(BaseModel):
    template_id: Optional[str] = None
    content: Optional[str] = None
    is_jsx: Optional[bool] = None  # Default to false for backward compatibility
    is_vue: Optional[bool] = None  # Default to false for backward compatibility
    data: Optional[dict] = None

class GuestUserResponse(BaseModel):
    id: int
    email: str
    password: str  # Include password in response
    is_active: bool = True
    is_guest: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
