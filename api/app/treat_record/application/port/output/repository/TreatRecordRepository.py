from abc import ABC, abstractmethod
from typing import List

from app.treat_record.application.port.input.CreateTreatRecordCommand import (
    CreateTreatRecordCommand,
)
from app.treat_record.application.port.input.UpdateTreatRecordCommand import (
    UpdateTreatRecordCommand,
)
from app.treat_record.domain.TreatRecord import TreatRecord


class TreatRecordRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateTreatRecordCommand) -> TreatRecord:
        pass

    @abstractmethod
    async def get(self, id: str, dog_id: str) -> TreatRecord:
        pass
    
    @abstractmethod
    async def get_all(self, dog_id: str) -> List[TreatRecord]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateTreatRecordCommand) -> TreatRecord:
        pass

    @abstractmethod
    async def delete(self, id: str, dog_id: str) -> None:
        pass