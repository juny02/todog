from pydantic import BaseModel


class UpdateTreatCommand(BaseModel):
    id: str
    dog_id: str
    name: str | None
    description: str | None