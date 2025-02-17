from pydantic import BaseModel


class AddDogFamilyCommand(BaseModel):
    dog_id: str
    user_id: str
    user_nickname: str | None
    dog_nickname: str | None