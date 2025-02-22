from pydantic import BaseModel


class UpdateTreatCommand(BaseModel):
    name: str | None
    dog_id: str | None
    description: str | None