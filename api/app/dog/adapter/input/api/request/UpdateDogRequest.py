from pydantic import BaseModel, ConfigDict

from app.dog.domain.Dog import DogSpecies


class UpdateDogRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    name: str | None = None
    age: int | None = None
    photo: str | None = None
    species: DogSpecies | None = None