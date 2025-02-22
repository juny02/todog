from pydantic import AwareDatetime, BaseModel


class CreateMealRecordCommand(BaseModel):
    dog_id: str
    user_id: str
    given_at: AwareDatetime
    meal_type: str | None
    amount: float | None
    photo_url: str | None
    description: str | None