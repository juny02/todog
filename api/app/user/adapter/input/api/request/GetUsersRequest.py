from pydantic import BaseModel, ConfigDict


class GetUsersRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    name: str | None = None
    email: str | None = None
    profile: str | None = None
    provider: str | None = None