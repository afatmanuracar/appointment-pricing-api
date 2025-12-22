from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models import Class as ClassModel
from app.auth import require_api_key

router = APIRouter()

class ClassCreate(BaseModel):
    name: str = Field(min_length=1)
    instructor: str = Field(min_length=1)
    capacity: int = Field(ge=1, le=200)
    start_time: datetime

class ClassOut(ClassCreate):
    id: str

@router.post(
    "",
    response_model=ClassOut,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_class(payload: ClassCreate, db: AsyncSession = Depends(get_db)):
    class_id = str(uuid4())
    clazz = ClassModel(
        id=class_id,
        name=payload.name,
        instructor=payload.instructor,
        capacity=payload.capacity,
        start_time=payload.start_time,
    )
    db.add(clazz)
    await db.commit()
    return ClassOut(id=clazz.id, **payload.model_dump())

@router.get("/{class_id}", response_model=ClassOut)
async def get_class(class_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ClassModel).where(ClassModel.id == class_id))
    clazz = res.scalar_one_or_none()
    if not clazz:
        raise HTTPException(status_code=404, detail="Class not found")
    return ClassOut(
        id=clazz.id,
        name=clazz.name,
        instructor=clazz.instructor,
        capacity=clazz.capacity,
        start_time=clazz.start_time,
    )
