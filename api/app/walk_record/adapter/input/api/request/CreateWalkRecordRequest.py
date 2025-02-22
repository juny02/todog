from pydantic import AwareDatetime, BaseModel, ConfigDict


class CreateWalkRecordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str
    start_time: AwareDatetime
    end_time: AwareDatetime
    description: str | None = None
    photo_url: str | None = None