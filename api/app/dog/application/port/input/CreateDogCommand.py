from pydantic import BaseModel

from app.dog.domain.Dog import DogMealPattern


class CreateDogCommand(BaseModel):
    name: str
    age: int | None
    photo: str | None
    species: str | None
    daily_walk_goal: int 
    meal_pattern: DogMealPattern