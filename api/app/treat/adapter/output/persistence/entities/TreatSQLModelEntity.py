from sqlmodel import Field, SQLModel

from core.db.utils.ulid import generate_ulid


class TreatSQLModelEntity(SQLModel, table=True):

    __tablename__ = "treat"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    dog_id: str = Field(nullable=False, max_length=32, foreign_key="dog.id")
    name: str = Field(nullable=False, max_length=32)
    description: str = Field(nullable=True, max_length=128)