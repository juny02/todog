from pydantic import BaseModel, ConfigDict


class AddDogFamilyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    dog_id: str
    user_id: str
    user_nickname: str | None = None
    dog_nickname: str | None = None