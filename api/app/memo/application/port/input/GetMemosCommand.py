from pydantic import AwareDatetime, BaseModel

from core.enums import SortOrder


class GetMemosCommand(BaseModel):
    dog_id: str 
    user_id: str | None
    content: str | None
    fixed: bool | None
    start: AwareDatetime | None = None 
    end: AwareDatetime | None = None 
    order: SortOrder