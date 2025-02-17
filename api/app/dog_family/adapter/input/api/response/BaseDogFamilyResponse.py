from pydantic import BaseModel


class BaseDogFamilyResponse(BaseModel):
    id: str
    dog_id: str
    user_id: str
    user_nickname: str | None
    dog_nickname: str | None

