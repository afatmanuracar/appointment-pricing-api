from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import engine
from app.models import Base

from app.api.members import router as members_router
from app.api.classes import router as classes_router
from app.api.reservations import router as reservations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown (istersen burada engine dispose vs. eklenebilir)


app = FastAPI(
    title="Appointment Pricing API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(members_router, prefix="/members", tags=["members"])
app.include_router(classes_router, prefix="/classes", tags=["classes"])
app.include_router(reservations_router, prefix="/reservations", tags=["reservations"])


@app.get("/health", tags=["default"])
async def health():
    return {"ok": True}
