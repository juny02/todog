from pydantic import AwareDatetime, BaseModel


class CreateWalkRecordCommand(BaseModel):
    dog_id: str
    user_id: str
    start_time: AwareDatetime
    end_time: AwareDatetime
    photo_url: str | None
    description: str | None
