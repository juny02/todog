from pydantic import BaseModel

from app.dog.domain.Dog import DogSpecies


class GetDogFamiliesCommand(BaseModel):
    name: str | None
    age: int | None
    photo: str | None
    species: DogSpecies | None 