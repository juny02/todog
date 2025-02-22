from pydantic import AwareDatetime, BaseModel


class UpdateWalkRecordCommand(BaseModel):
    id: str
    dog_id: str
    
    user_id: str | None
    start_time: AwareDatetime | None
    end_time: AwareDatetime | None
    photo_url: str | None
    description: str | None
