from pydantic import AwareDatetime, BaseModel


class CreateTreatRecordCommand(BaseModel):
    dog_id: str
    user_id: str
    treat_id: str
    quantity: int
    given_at: AwareDatetime
    description: str | None
    photo_url: str | None
