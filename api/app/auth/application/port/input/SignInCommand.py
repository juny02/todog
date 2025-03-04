from pydantic import BaseModel


class SignInCommand(BaseModel):
    email: str
    password: str
