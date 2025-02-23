from datetime import datetime

from sqlmodel import Field, SQLModel

from core.db.utils.ulid import generate_ulid


class ScheduleSQLModelEntity(SQLModel, table=True):

    __tablename__ = "schedule"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    dog_id: str = Field(nullable=False, max_length=32, foreign_key="dog.id")
    title: str = Field(nullable=False, max_length=128)
    content: str = Field(nullable=True, max_length=256)
    complete: bool = Field(nullable=False, default=False)
    scheduled_at: datetime = Field(default_factory=datetime.now, nullable=False)
