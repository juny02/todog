from pydantic import AwareDatetime, BaseModel, ConfigDict


class CreateMealRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str
    given_at: AwareDatetime
    meal_type: str | None = None
    amount: float | None = None
    description: str | None = None
    photo_url: str | None = None