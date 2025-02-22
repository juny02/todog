from pydantic import BaseModel, ConfigDict


class CreateTreatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str
    description: str | None = None

