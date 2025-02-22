from pydantic import AwareDatetime, BaseModel


class UpdateTreatRecordCommand(BaseModel):
    id: str
    dog_id: str
    
    user_id: str | None
    treat_id: str | None
    quantity: int | None
    given_at: AwareDatetime | None
    description: str | None
