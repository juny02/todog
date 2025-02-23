from pydantic import AwareDatetime, BaseModel, ConfigDict

from core.enums import SortOrder


class GetMemosRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    user_id: str | None = None
    content: str | None = None
    fixed: bool | None = None
    start: AwareDatetime | None = None 
    end: AwareDatetime | None = None 
    order: SortOrder = SortOrder.DESC