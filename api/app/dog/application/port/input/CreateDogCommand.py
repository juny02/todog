from pydantic import BaseModel

from app.dog.domain.Dog import DogSpecies


class CreateDogCommand(BaseModel):
    name: str
    age: int | None
    photo: str | None
    species: str | None
