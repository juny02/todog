from pydantic import BaseModel

from app.dog.domain.Dog import DogMealPattern


class GetDogsCommand(BaseModel):
    name: str | None
    age: int | None
    photo: str | None
    species: str | None 
    daily_walk_goal: int | None = None
    meal_pattern: DogMealPattern | None = None