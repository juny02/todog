from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    provider: str | None
    email: str | None
    profile: str | None
