from pydantic import AwareDatetime, BaseModel, ConfigDict

from core.enums import SortOrder


class GetSchedulesRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    title: str | None = None
    content: str | None = None
    complete: bool | None = None
    scheduled_at: AwareDatetime | None = None
    
    start: AwareDatetime | None = None 
    end: AwareDatetime | None = None 
    order: SortOrder = SortOrder.DESC