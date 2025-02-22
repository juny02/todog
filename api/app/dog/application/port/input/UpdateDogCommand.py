from pydantic import BaseModel

from app.dog.domain.Dog import DogMealPattern


class UpdateDogCommand(BaseModel):
    id: str | None = None
    name: str | None = None
    age: int | None = None
    photo: str | None = None
    species: str | None = None
    daily_walk_goal: int | None = None
    meal_pattern: DogMealPattern | None = None