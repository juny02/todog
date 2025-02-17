from sqlalchemy import Column, Enum
from sqlmodel import Field, SQLModel

from app.dog.domain.Dog import DogSpecies
from core.db.utils.ulid import generate_ulid


class DogSQLModelEntity(SQLModel, table=True):

    __tablename__ = "dog"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    name: str = Field(nullable=False, max_length=32)
    age: int = Field(nullable=True)
    photo: str = Field(nullable=True, max_length=32)
    species: DogSpecies = Field(sa_column=Column(Enum(DogSpecies)))
