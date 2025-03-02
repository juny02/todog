from enum import Enum
from typing import List

from pydantic import AwareDatetime, BaseModel


class MedType(str, Enum):
    ONCE = "once"
    RECURRING = "recurring"
    TEMPORARY = "temporary"


class MedSchedule(BaseModel):
    id: str
    dog_id: str
    medicine_name: str
    dosage: str | None 
    daily_doses: int 
    dose_times : List[str]
    type: MedType 
    interval_days: int | None
    start: AwareDatetime
    end: AwareDatetime | None
    notes: str | None 
