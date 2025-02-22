from pydantic import AwareDatetime, BaseModel


class MealRecord(BaseModel):
    id: str
    dog_id: str
    user_id: str
    given_at: AwareDatetime
    meal_type: str | None
    amount: float | None
    photo_url: str | None
    description: str | None