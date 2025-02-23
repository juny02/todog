from pydantic import AwareDatetime, BaseModel, ConfigDict


class UpdateMemoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str | None = None
    content: str | None = None
    fixed: bool | None = None
    created_at: AwareDatetime | None = None
