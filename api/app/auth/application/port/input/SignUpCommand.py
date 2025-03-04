from pydantic import BaseModel

from app.feature.auth.domain import UserLevel


class SignUpCommand(BaseModel):
    name: str
    email: str
    password: str
    profile: str | None 
    provider: str | None