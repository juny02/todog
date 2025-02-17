from sqlmodel import Field, SQLModel

from core.db.utils.ulid import generate_ulid


class DogFamilySQLModelEntity(SQLModel, table=True):

    __tablename__ = "dog_family"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    dog_id: str = Field(nullable=False, max_length=32, foreign_key="dog.id")
    user_id: str = Field(nullable=False, max_length=32, foreign_key="user.id")
    user_nickname: str = Field(nullable=True, max_length=16)
    dog_nickname: str = Field(nullable=True, max_length=16)