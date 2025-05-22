from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# User schemas
class UserBase(BaseModel):
    email: str
    name: str
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
