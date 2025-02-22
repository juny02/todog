from enum import Enum

from pydantic import BaseModel


class DogSpecies(str, Enum):
    POODLE = "poodle"
    GOLDEN_RETRIEVER = "golden_retriever"
    BULLDOG = "bulldog"
    BEAGLE = "beagle"
    GERMAN_SHEPHERD = "german_shepherd"
    SHIBA_INU = "shiba_inu"
    DACHSHUND = "dachshund"
    HUSKY = "husky"
    LABRADOR = "labrador"
    CHIHUAHUA = "chihuahua"


class Dog(BaseModel):
    id: str
    name: str
    age: int | None
    photo: str | None
