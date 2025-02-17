from abc import ABC, abstractmethod
from typing import List

from api.app.dog_family.application.port.input.GetDogFamiliesCommand import GetDogFamiliesCommand

from app.dog_family.application.port.input.AddDogFamilyCommand import AddDogFamilyCommand
from app.dog_family.application.port.input.UpdateDogFamilyCommand import UpdateDogFamilyCommand
from app.dog_family.domain.DogFamily import DogFamily


class DogFamilyRepository(ABC):
    @abstractmethod
    async def create(self, cmd: AddDogFamilyCommand) -> DogFamily:
        pass

    @abstractmethod
    async def get(self, id: str) -> DogFamily:
        pass
    
    @abstractmethod
    async def get_all(self, cmd: GetDogFamiliesCommand) -> List[DogFamily]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateDogFamilyCommand) -> DogFamily:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass