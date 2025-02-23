
from pydantic import AwareDatetime, BaseModel


class Memo(BaseModel):
    id: str
    dog_id: str
    user_id: str
    content: str
    fixed: bool = False
    created_at: AwareDatetime
