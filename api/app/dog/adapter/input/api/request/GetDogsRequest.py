from pydantic import BaseModel, ConfigDict


class GetDogsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    name: str | None = None
    age: int | None = None
    photo: str | None = None
    species: str | None = None