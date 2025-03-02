from abc import ABC, abstractmethod
from typing import List

from app.medicine_record.application.port.input.CreateMedRecordCommand import CreateMedRecordCommand
from app.medicine_record.application.port.input.GetMedRecordsCommand import GetMedRecordsCommand
from app.medicine_record.application.port.input.UpdateMedRecordCommand import UpdateMedRecordCommand
from app.medicine_record.domain.MedRecord import MedRecord


class MedRecordRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateMedRecordCommand) -> MedRecord:
        pass

    @abstractmethod
    async def get(self, id: str, dog_id: str) -> MedRecord:
        pass
    
    @abstractmethod
    async def get_all(self, cmd: GetMedRecordsCommand) -> List[MedRecord]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateMedRecordCommand) -> MedRecord:
        pass

    @abstractmethod
    async def delete(self, id: str, dog_id: str) -> None:
        pass