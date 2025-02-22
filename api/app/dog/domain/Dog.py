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

class DogMealPattern(str, Enum):
    ONE_MEAL = "one_meal"
    TWO_MEALS = "two_meals"
    THREE_MEALS = "three_meals"
    FREE_FEEDING = "free_feeding"

class Dog(BaseModel):
    id: str
    name: str
    age: int | None
    photo: str | None
    species: str | None
    daily_walk_goal: int
    meal_pattern: DogMealPattern
