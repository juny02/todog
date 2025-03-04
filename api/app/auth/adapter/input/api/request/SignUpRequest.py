from pydantic import BaseModel


class SignUpBodyParams(BaseModel):
    name: str
    email: str
    password: str
    profile: str | None = None
    provider: str | None = None
