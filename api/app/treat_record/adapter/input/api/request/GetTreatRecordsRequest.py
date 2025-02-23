from pydantic import AwareDatetime, BaseModel, ConfigDict

from core.enums import SortOrder


class GetTreatRecordsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str | None = None
    treat_id: str | None = None
    description: str | None = None
    start: AwareDatetime | None = None
    end: AwareDatetime | None = None
    order: SortOrder = SortOrder.ASC