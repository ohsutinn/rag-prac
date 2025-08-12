from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# 2) 비동기 엔진
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,          
    pool_pre_ping=True, 
)

# 3) 비동기 세션팩토리
AsyncSessionFactory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)