from pydantic import BaseModel, ConfigDict

from app.dog.domain.Dog import DogMealPattern


class CreateDogRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    name: str
    age: int | None = None
    photo: str | None = None
    species: str | None = None
    daily_walk_goal: int
    meal_pattern: DogMealPattern
    
