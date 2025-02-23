from pydantic import AwareDatetime, BaseModel


class UpdateMemoCommand(BaseModel):
    id: str
    dog_id: str
    
    user_id: str | None
    content: str | None
    fixed: bool | None
    created_at: AwareDatetime | None