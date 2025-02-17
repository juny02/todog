from pydantic import BaseModel


class UpdateDogFamilyCommand(BaseModel):
    id: str
    dog_id: str | None
    user_id: str | None
    user_nickname: str | None
    dog_nickname: str | None 
