from abc import ABC, abstractmethod
from typing import List

from app.treat.application.port.input.CreateTreatCommand import CreateTreatCommand
from app.treat.application.port.input.UpdateTreatCommand import UpdateTreatCommand
from app.treat.domain.Treat import Treat


class TreatRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateTreatCommand) -> Treat:
        pass

    @abstractmethod
    async def get(self, id: str, dog_id: str) -> Treat:
        pass
    
    @abstractmethod
    async def get_all_by_dog(self, dog_id: str) -> List[Treat]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateTreatCommand) -> Treat:
        pass

    @abstractmethod
    async def delete(self, id: str, dog_id: str) -> None:
        pass