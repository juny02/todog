from fastapi import Depends

from app.meal_record.adapter.output.persistence.repository.MealRecordSQLModelRepository import (
    MealRecordSQLModelRepository,
)
from app.meal_record.application.port.output.repository.MealRecordRepository import (
    MealRecordRepository,
)
from app.meal_record.domain.MealRecord import MealRecord


class GetMealRecordUseCase:
    def __init__(self, meal_record_repo: MealRecordRepository = Depends(MealRecordSQLModelRepository)):
        self.meal_record_repo = meal_record_repo

    async def __call__(self, id: str, dog_id: str) -> MealRecord:
        return await self.meal_record_repo.get(id=id, dog_id=dog_id)
