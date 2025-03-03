from sqlmodel import Field, SQLModel

from core.db.utils.ulid import generate_ulid


class UserSQLModelEntity(SQLModel, table=True):

    __tablename__ = "user"

    id: str = Field(primary_key=True, nullable=False, default_factory=generate_ulid)
    name: str = Field(nullable=False, max_length=32)
    password: str = Field(nullable=True, max_length=1024)
    provider: str = Field(nullable=True, max_length=32)
    email: str = Field(nullable=True, max_length=64)
    profile: str = Field(nullable=True, max_length=256)
