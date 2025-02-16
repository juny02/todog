from pydantic import BaseModel

from app.dog.adapter.input.api.response.BaseDogResponse import BaseDogResponse
from app.dog.domain.Dog import DogSpecies


class GetDogResponse(BaseDogResponse):
    pass
