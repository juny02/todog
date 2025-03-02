from pydantic import AwareDatetime, BaseModel

from app.medicine_schedule.domain.MedSchedule import MedType
from core.enums import SortOrder


class GetMedSchedulesCommand(BaseModel):
    dog_id: str 
    
    medicine_name: str | None  
    dosage: str | None  
    daily_doses: int | None  
    type: MedType | None  
    interval_days: int | None  
    start: AwareDatetime | None  
    end: AwareDatetime | None  
    date: AwareDatetime | None 
    order: SortOrder 