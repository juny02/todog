from pydantic import BaseModel, ConfigDict


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    name: str 
    email: str | None = None
    profile: str | None = None
    provider: str | None = None