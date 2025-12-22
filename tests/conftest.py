import os
import tempfile

import pytest
import httpx
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.models import Base
from app.api.deps import get_db


@pytest.fixture
async def client():
    # 1) Her test için ayrı sqlite dosyası
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    test_db_url = f"sqlite+aiosqlite:///{db_path}"

    # 2) Test engine + sessionmaker
    engine = create_async_engine(test_db_url, echo=False, future=True)
    TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # 3) Tabloları test DB'de oluştur
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 4) get_db override (test DB session)
    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    # 5) httpx AsyncClient (ASGI)
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # 6) Temizlik
    app.dependency_overrides.clear()
    await engine.dispose()
    try:
        os.remove(db_path)
    except OSError:
        pass
