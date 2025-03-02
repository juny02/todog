from typing import List

from pydantic import AwareDatetime, BaseModel

from app.medicine_schedule.domain.MedSchedule import MedType


class UpdateMedScheduleCommand(BaseModel):
    id: str
    dog_id: str
    
    medicine_name: str | None
    dosage: str | None
    daily_doses: int | None
    dose_times : List[str] | None
    type: MedType | None
    interval_days: int | None
    start: AwareDatetime | None
    end: AwareDatetime | None
    notes: str | None