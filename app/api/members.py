from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from enum import Enum
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.models import Member
from app.auth import require_api_key

router = APIRouter()

class MembershipType(str, Enum):
    standard = "standard"
    premium = "premium"
    student = "student"

class MemberCreate(BaseModel):
    name: str = Field(min_length=1)
    membership_type: MembershipType

class MemberOut(MemberCreate):
    id: str

@router.post(
    "",
    response_model=MemberOut,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_member(payload: MemberCreate, db: AsyncSession = Depends(get_db)):
    member_id = str(uuid4())
    member = Member(
        id=member_id,
        name=payload.name,
        membership_type=payload.membership_type.value,
    )
    db.add(member)
    await db.commit()
    return MemberOut(
        id=member.id,
        name=member.name,
        membership_type=payload.membership_type,
    )

@router.get("/{member_id}", response_model=MemberOut)
async def get_member(member_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Member).where(Member.id == member_id))
    member = res.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberOut(
        id=member.id,
        name=member.name,
        membership_type=member.membership_type,
    )
