from pydantic import BaseModel


class UpdateDogFamilyCommand(BaseModel):
    dog_id: str | None
    user_id: str | None
    user_nickname: str | None
    dog_nickname: str | None 
