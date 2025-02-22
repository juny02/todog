from abc import ABC, abstractmethod
from typing import List

from app.walk_record.application.port.input.CreateWalkRecordCommand import CreateWalkRecordCommand
from app.walk_record.application.port.input.UpdateWalkRecordCommand import UpdateWalkRecordCommand
from app.walk_record.domain.WalkRecord import WalkRecord


class WalkRecordRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateWalkRecordCommand) -> WalkRecord:
        pass

    @abstractmethod
    async def get(self, id: str, dog_id: str) -> WalkRecord:
        pass
    
    @abstractmethod
    async def get_all_by_dog(self, dog_id: str) -> List[WalkRecord]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateWalkRecordCommand) -> WalkRecord:
        pass

    @abstractmethod
    async def delete(self, id: str, dog_id: str) -> None:
        pass