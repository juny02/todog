from pydantic import AwareDatetime, BaseModel


class BaseMemoResponse(BaseModel):
    id: str
    dog_id: str
    user_id: str
    content: str
    fixed: bool 
    created_at: AwareDatetime

