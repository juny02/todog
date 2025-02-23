from pydantic import AwareDatetime, BaseModel


class Schedule(BaseModel):
    id: str
    dog_id: str
    title: str
    content: str | None
    complete: bool = False
    scheduled_at: AwareDatetime
