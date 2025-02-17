from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    name: str
    provider: str | None
    email: str | None
    profile: str | None
