from datetime import datetime

from sqlmodel import Field, SQLModel

from core.db.utils.ulid import generate_ulid


class MealRecordSQLModelEntity(SQLModel, table=True):

    __tablename__ = "meal_record"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    dog_id: str = Field(nullable=False, max_length=32, foreign_key="dog.id")
    user_id: str = Field(nullable=False, max_length=32, foreign_key="user.id")
    given_at: datetime = Field(default_factory=datetime.now, nullable=False)
    meal_type: str = Field(nullable=True, max_length=32)
    amount: float = Field(nullable=True)
    description: str = Field(nullable=True, max_length=256)
    photo_url: str = Field(nullable=True, max_length=512)
