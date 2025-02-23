from pydantic import AwareDatetime, BaseModel


class CreateScheduleCommand(BaseModel):
    dog_id: str
    title: str
    content: str | None
    complete: bool
    scheduled_at: AwareDatetime
