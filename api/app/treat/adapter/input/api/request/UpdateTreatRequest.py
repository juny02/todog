from pydantic import BaseModel, ConfigDict


class UpdateTreatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str | None = None
    description: str | None = None
