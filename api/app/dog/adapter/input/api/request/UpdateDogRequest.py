from pydantic import BaseModel, ConfigDict

from app.dog.domain.Dog import DogMealPattern


class UpdateDogRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str | None = None
    age: int | None = None
    photo: str | None = None
    species: str | None = None
    daily_walk_goal: int | None = None
    meal_pattern: DogMealPattern | None = None
