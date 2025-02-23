from abc import ABC, abstractmethod
from typing import List

from app.meal_record.application.port.input.CreateMealRecordCommand import CreateMealRecordCommand
from app.meal_record.application.port.input.GetMealRecordsCommand import GetMealRecordsCommand
from app.meal_record.application.port.input.UpdateMealRecordCommand import UpdateMealRecordCommand
from app.meal_record.domain.MealRecord import MealRecord


class MealRecordRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateMealRecordCommand) -> MealRecord:
        pass

    @abstractmethod
    async def get(self, id: str, dog_id: str) -> MealRecord:
        pass
    
    @abstractmethod
    async def get_all(self, cmd: GetMealRecordsCommand) -> List[MealRecord]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateMealRecordCommand) -> MealRecord:
        pass

    @abstractmethod
    async def delete(self, id: str, dog_id: str) -> None:
        pass