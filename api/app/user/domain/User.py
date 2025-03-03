from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    password: str | None
    provider: str | None
    email: str
    profile: str | None
