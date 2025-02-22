from pydantic import BaseModel


class BaseTreatResponse(BaseModel):
    id: str
    name: str
    dog_id: str
    description: str | None
