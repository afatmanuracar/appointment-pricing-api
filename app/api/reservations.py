from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api.deps import get_db
from app.models import Member, Class as ClassModel, Reservation as ReservationModel
from app.domain.pricing import PricingInput, price_for
from app.auth import require_api_key

router = APIRouter()

class ReservationCreate(BaseModel):
    member_id: str
    class_id: str
    base_price: float = Field(gt=0)

class ReservationOut(BaseModel):
    id: str
    member_id: str
    class_id: str
    final_price: float
    created_at: datetime

@router.post(
    "",
    response_model=ReservationOut,
    status_code=201,
    dependencies=[Depends(require_api_key)],
)
async def create_reservation(payload: ReservationCreate, db: AsyncSession = Depends(get_db)):
    # Member
    m_res = await db.execute(select(Member).where(Member.id == payload.member_id))
    member = m_res.scalar_one_or_none()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # Class
    c_res = await db.execute(select(ClassModel).where(ClassModel.id == payload.class_id))
    clazz = c_res.scalar_one_or_none()
    if not clazz:
        raise HTTPException(status_code=404, detail="Class not found")

    # Capacity
    count_res = await db.execute(
        select(func.count()).select_from(ReservationModel).where(
            ReservationModel.class_id == payload.class_id
        )
    )
    current = int(count_res.scalar_one())
    if current >= clazz.capacity:
        raise HTTPException(status_code=409, detail="Class capacity full")

    occupancy = (current + 1) / clazz.capacity

    final_price = price_for(
        PricingInput(
            membership_type=member.membership_type,
            base_price=payload.base_price,
            occupancy_rate=occupancy,
            start_time=clazz.start_time,
        )
    )

    reservation_id = str(uuid4())
    created_at = datetime.utcnow()

    reservation = ReservationModel(
        id=reservation_id,
        member_id=payload.member_id,
        class_id=payload.class_id,
        base_price=payload.base_price,
        final_price=final_price,
        created_at=created_at,
    )
    db.add(reservation)
    await db.commit()

    return ReservationOut(
        id=reservation_id,
        member_id=payload.member_id,
        class_id=payload.class_id,
        final_price=final_price,
        created_at=created_at,
    )
