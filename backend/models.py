from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum, ForeignKey, Text, JSON
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyBaseOAuthAccountTable
from database import Base
from nanoid import generate
import enum

class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    __tablename__ = "oauth_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    # oauth_name, access_token, expires_at, account_id, account_email are inherited
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)
    user = relationship("User", back_populates="oauth_accounts")


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    
    # Explicitly define id column to match existing database schema
    id = Column(Integer, primary_key=True, index=True)
    # email, hashed_password, is_active, is_superuser, is_verified are inherited from SQLAlchemyBaseUserTable
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_guest = Column(Boolean, default=False)
    
    # Relationships
    templates = relationship("Template", backref="users")
    oauth_accounts = relationship("OAuthAccount", back_populates="user")


class TemplatingEngineEnum(str, Enum):
    JSX = "jsx"
    HTML = "html"
    VUE = "vue"


class Template(Base):
    __tablename__ = "templates"
    id = Column(String(10), primary_key=True, default=lambda: generate(size=10), index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    engine = Column(SQLEnum(TemplatingEngineEnum), default=TemplatingEngineEnum.HTML)
    content = Column(Text)
    data = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))



'''
For Future
class TemplateStats(Base):
    id
    action
    ip 
    created_at
    updated_at
    
'''