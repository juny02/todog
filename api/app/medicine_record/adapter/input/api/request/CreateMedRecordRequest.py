from pydantic import AwareDatetime, BaseModel, ConfigDict


class CreateMedRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str
    given_at: AwareDatetime
    schedule_id: str | None = None
    dose_given: str | None = None
    photo_url: str | None = None
    description: str | None = None