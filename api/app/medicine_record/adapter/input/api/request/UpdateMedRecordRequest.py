from pydantic import AwareDatetime, BaseModel, ConfigDict


class UpdateMedRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str | None = None
    given_at: AwareDatetime | None = None
    schedule_id: str | None = None
    dose_given: str | None = None
    photo_url: str | None = None
    description: str | None = None
