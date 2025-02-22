from pydantic import BaseModel, ConfigDict

from app.dog.domain.Dog import DogSpecies


class CreateDogRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    name: str
    age: int | None = None
    photo: str | None = None
    species: str | None = None
