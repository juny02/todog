from pydantic import AwareDatetime, BaseModel, ConfigDict


class CreateMemoRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    
    user_id: str
    content: str 
    fixed: bool = False
    created_at: AwareDatetime