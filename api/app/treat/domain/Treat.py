from pydantic import BaseModel


class Treat(BaseModel):
    id: str
    dog_id: str
    name: str
    description: str | None
