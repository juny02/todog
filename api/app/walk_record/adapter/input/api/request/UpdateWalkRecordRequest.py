from pydantic import AwareDatetime, BaseModel, ConfigDict


class UpdateWalkRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str | None = None
    start_time: AwareDatetime | None = None
    end_time: AwareDatetime | None = None
    description: str | None = None
    photo_url: str | None = None
