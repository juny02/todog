from pydantic import AwareDatetime, BaseModel

from core.enums import SortOrder


class GetWalkRecordsCommand(BaseModel):
    dog_id: str 
    
    user_id: str | None
    description: str | None
    
    start: AwareDatetime | None
    end: AwareDatetime | None
    order: SortOrder