"""
Database configuration and session management
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

# Convert SQLite URL to async format
if DATABASE_URL.startswith("sqlite://"):
    SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
else:
    SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create async SessionLocal class
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
