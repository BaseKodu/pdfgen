from pydantic import BaseModel, Json
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi_users import schemas
from enum import Enum



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
    data: Optional[dict] = None
