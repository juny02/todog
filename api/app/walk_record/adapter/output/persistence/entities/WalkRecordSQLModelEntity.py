from datetime import datetime

from sqlmodel import Field, SQLModel

from core.db.utils.ulid import generate_ulid


class WalkRecordSQLModelEntity(SQLModel, table=True):

    __tablename__ = "walk_record"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    dog_id: str = Field(nullable=False, max_length=32, foreign_key="dog.id")
    user_id: str = Field(nullable=False, max_length=32, foreign_key="user.id")
    start_time: datetime = Field(default_factory=datetime.now, nullable=False)
    end_time: datetime = Field(default_factory=datetime.now, nullable=False)
    description: str = Field(nullable=True, max_length=256)
    photo_url: str = Field(nullable=True, max_length=512)
