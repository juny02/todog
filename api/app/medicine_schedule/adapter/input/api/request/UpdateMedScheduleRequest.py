from typing import List

from pydantic import AwareDatetime, BaseModel, ConfigDict

from app.medicine_schedule.domain.MedSchedule import MedType


class UpdateMedScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    medicine_name: str | None = None
    dosage: str | None = None
    daily_doses: int | None = None
    dose_times : List[str] | None = None
    type: MedType | None = None
    interval_days: int | None = None
    start: AwareDatetime | None = None
    end: AwareDatetime | None = None
    notes: str | None = None