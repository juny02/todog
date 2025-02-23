from pydantic import AwareDatetime, BaseModel

from core.enums import SortOrder


class GetSchedulesCommand(BaseModel):
    dog_id: str 
    
    title: str | None
    content: str | None
    complete: bool | None
    scheduled_at: AwareDatetime | None
    
    start: AwareDatetime | None = None 
    end: AwareDatetime | None = None 
    order: SortOrder