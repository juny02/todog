from pydantic import AwareDatetime, BaseModel


class BaseMedRecordResponse(BaseModel):
    id: str
    dog_id: str
    user_id: str
    given_at: AwareDatetime
    schedule_id: str | None
    dose_given: str | None
    photo_url: str | None
    description: str | None