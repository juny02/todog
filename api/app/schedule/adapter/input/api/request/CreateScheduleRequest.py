from pydantic import AwareDatetime, BaseModel, ConfigDict


class CreateScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    title: str
    content: str | None = None
    complete: bool = False
    scheduled_at: AwareDatetime