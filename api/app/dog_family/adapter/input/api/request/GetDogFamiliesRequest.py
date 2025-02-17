from pydantic import BaseModel, ConfigDict


class GetDogFamiliesRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    dog_id: str | None = None
    user_id: str | None = None
    user_nickname: str | None = None
    dog_nickname: str | None = None