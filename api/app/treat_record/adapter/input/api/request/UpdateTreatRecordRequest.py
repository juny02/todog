from pydantic import AwareDatetime, BaseModel, ConfigDict


class UpdateTreatRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str | None = None
    treat_id: str | None = None
    quantity: int | None = None
    given_at: AwareDatetime | None = None
    description: str | None = None
    photo_url: str | None = None
