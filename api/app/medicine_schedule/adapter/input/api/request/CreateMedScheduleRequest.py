from typing import List

from pydantic import AwareDatetime, BaseModel, ConfigDict

from app.medicine_schedule.domain.MedSchedule import MedType


class CreateMedScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    medicine_name: str
    dosage: str | None = None
    daily_doses: int = 1 
    dose_times : List[str] = []
    type: MedType 
    interval_days: int | None = None
    start: AwareDatetime | None = None
    end: AwareDatetime | None = None
    notes: str | None = None