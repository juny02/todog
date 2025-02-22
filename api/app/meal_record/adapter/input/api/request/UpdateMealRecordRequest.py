from pydantic import AwareDatetime, BaseModel, ConfigDict


class UpdateMealRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str | None = None
    given_at: AwareDatetime | None = None
    meal_type: str | None = None
    amount: float | None = None
    description: str | None = None
    photo_url: str | None = None
