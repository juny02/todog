from pydantic import AwareDatetime, BaseModel


class UpdateScheduleCommand(BaseModel):
    id: str
    dog_id: str
    
    title: str | None
    content: str | None
    complete: bool | None
    scheduled_at: AwareDatetime | None