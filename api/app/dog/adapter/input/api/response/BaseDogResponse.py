from pydantic import BaseModel

from app.dog.domain.Dog import DogSpecies


class BaseDogResponse(BaseModel):
    id: str
    name: str
    age: int | None
    photo: str | None
    species: str | None
