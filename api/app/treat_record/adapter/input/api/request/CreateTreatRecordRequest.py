from pydantic import AwareDatetime, BaseModel, ConfigDict


class CreateTreatRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str
    treat_id: str
    quantity: int
    given_at: AwareDatetime
    description: str | None = None
    photo_url: str | None = None