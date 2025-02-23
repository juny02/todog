from pydantic import AwareDatetime, BaseModel


class CreateMemoCommand(BaseModel):
    dog_id: str
    user_id: str
    content: str
    fixed: bool
    created_at: AwareDatetime
