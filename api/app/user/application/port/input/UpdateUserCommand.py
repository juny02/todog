from pydantic import BaseModel


class UpdateUserCommand(BaseModel):
    id: str
    name: str | None
    provider: str | None
    email: str | None
    profile: str | None
