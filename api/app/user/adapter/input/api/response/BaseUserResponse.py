from pydantic import BaseModel


class BaseUserResponse(BaseModel):
    id: str
    name: str 
    email: str | None 
    profile: str | None 
    provider: str | None 