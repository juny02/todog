from pydantic import BaseModel

from app.dog.domain.Dog import DogSpecies


class UpdateDogCommand(BaseModel):
    id: str | None = None
    name: str | None = None
    age: int | None = None
    photo: str | None = None
    species: str | None = None
