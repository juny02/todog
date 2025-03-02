from pydantic import AwareDatetime, BaseModel, ConfigDict

from app.medicine_schedule.domain.MedSchedule import MedType
from core.enums import SortOrder


class GetMedSchedulesRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    medicine_name: str | None = None 
    dosage: str | None = None 
    daily_doses: int | None = None 
    type: MedType | None = None 
    interval_days: int | None = None 
    start: AwareDatetime | None = None 
    end: AwareDatetime | None = None 
    date: AwareDatetime | None = None # 이날짜에 포함되는 스케줄 보내주기 위함 (start<=date<=end)
    order: SortOrder = SortOrder.DESC