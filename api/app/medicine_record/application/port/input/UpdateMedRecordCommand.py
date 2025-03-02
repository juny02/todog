from pydantic import AwareDatetime, BaseModel


class UpdateMedRecordCommand(BaseModel):
    id: str
    dog_id: str
    
    user_id: str | None
    given_at: AwareDatetime | None
    schedule_id: str | None
    dose_given: str | None
    photo_url: str | None
    description: str | None
