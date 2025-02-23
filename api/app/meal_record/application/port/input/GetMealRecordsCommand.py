from pydantic import AwareDatetime, BaseModel

from core.enums import SortOrder


class GetMealRecordsCommand(BaseModel):
    dog_id: str 
    
    user_id: str | None
    meal_type: str | None
    description: str | None
    start: AwareDatetime | None
    end: AwareDatetime | None
    order: SortOrder