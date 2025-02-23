from datetime import datetime

from sqlmodel import Field, SQLModel

from core.db.utils.ulid import generate_ulid


class MemoSQLModelEntity(SQLModel, table=True):

    __tablename__ = "memo"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    dog_id: str = Field(nullable=False, max_length=32, foreign_key="dog.id")
    user_id: str = Field(nullable=False, max_length=32, foreign_key="user.id")
    content: str = Field(nullable=False, max_length=256)
    fixed: bool = Field(nullable=False, default=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
