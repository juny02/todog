from typing import List

from pydantic import AwareDatetime, BaseModel

from app.medicine_schedule.domain.MedSchedule import MedType


class CreateMedScheduleCommand(BaseModel):
    dog_id: str
    
    medicine_name: str
    dosage: str | None 
    daily_doses: int = 1 
    dose_times : List[str]
    type: MedType 
    interval_days: int | None 
    start: AwareDatetime | None
    end: AwareDatetime | None
    notes: str | None