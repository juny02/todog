from pydantic import AwareDatetime, BaseModel


class UpdateMealRecordCommand(BaseModel):
    id: str
    dog_id: str
    
    user_id: str | None
    given_at: AwareDatetime | None
    meal_type: str | None
    amount: float | None
    photo_url: str | None
    description: str | None
