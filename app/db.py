from __future__ import annotations

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
