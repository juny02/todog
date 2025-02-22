from pydantic import BaseModel


class CreateTreatCommand(BaseModel):
    name: str 
    dog_id: str
    description: str | None 