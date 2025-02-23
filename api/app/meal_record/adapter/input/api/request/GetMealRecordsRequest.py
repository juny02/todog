from pydantic import AwareDatetime, BaseModel, ConfigDict

from core.enums import SortOrder


class GetMealRecordsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str | None = None
    meal_type: str | None = None
    description: str | None = None
    start: AwareDatetime | None = None
    end: AwareDatetime | None = None
    order: SortOrder = SortOrder.ASC