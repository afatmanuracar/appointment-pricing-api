from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Member(Base):
    __tablename__ = "members"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    membership_type: Mapped[str] = mapped_column(String, nullable=False)

class Class(Base):
    __tablename__ = "classes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    instructor: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), nullable=False)
    class_id: Mapped[str] = mapped_column(ForeignKey("classes.id"), nullable=False)
    base_price: Mapped[float] = mapped_column(Float, nullable=False)
    final_price: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    member = relationship("Member")
    clazz = relationship("Class")
