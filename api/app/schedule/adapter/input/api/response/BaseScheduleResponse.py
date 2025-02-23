from pydantic import AwareDatetime, BaseModel


class BaseScheduleResponse(BaseModel):
    id: str
    dog_id: str
    title: str
    content: str | None
    complete: bool 
    scheduled_at: AwareDatetime

