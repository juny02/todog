from pydantic import BaseModel


class GetUsersCommand(BaseModel):
    name: str | None
    provider: str | None
    email: str | None
    profile: str | None
