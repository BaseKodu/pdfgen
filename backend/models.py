from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum, ForeignKey, Text, JSON
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
from database import Base
from nanoid import generate
import enum

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    # email, hashed_password, is_active, is_superuser, is_verified are inherited
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    templates = relationship("Template", backref="users")


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