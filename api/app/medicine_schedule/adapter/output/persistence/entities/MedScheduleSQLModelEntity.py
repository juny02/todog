from datetime import datetime
from typing import List

from sqlmodel import JSON, Column, Enum, Field, SQLModel

from app.medicine_schedule.domain.MedSchedule import MedType
from core.db.utils.ulid import generate_ulid


class MedScheduleSQLModelEntity(SQLModel, table=True):

    __tablename__ = "medicine_schedule"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    dog_id: str = Field(nullable=False, max_length=32, foreign_key="dog.id")
    medicine_name: str = Field(nullable=False, max_length=32)
    dosage: str | None = Field(nullable=True, max_length=32)
    daily_doses: int = Field(nullable=False, default=1)
    dose_times: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    type: MedType = Field(sa_column=Column(Enum(MedType)))
    interval_days: int | None = Field(nullable=True, default=None)
    start: datetime = Field(default_factory=datetime.now, nullable=False)
    end: datetime | None = Field(default=None, nullable=True)
    notes: str | None = Field(default=None, nullable=True, max_length=256)