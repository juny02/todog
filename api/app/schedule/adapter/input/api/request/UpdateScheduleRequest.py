from pydantic import AwareDatetime, BaseModel, ConfigDict


class UpdateScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    title: str | None = None
    content: str | None = None
    complete: bool | None = None
    scheduled_at: AwareDatetime | None = None
