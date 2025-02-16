from abc import ABC, abstractmethod
from typing import List

from app.dog.application.port.input.CreateDogCommand import CreateDogCommand
from app.dog.application.port.input.GetDogsCommand import GetDogsCommand
from app.dog.application.port.input.UpdateDogCommand import UpdateDogCommand
from app.dog.domain.Dog import Dog


class DogRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateDogCommand) -> Dog:
        pass

    @abstractmethod
    async def get(self, id: str) -> Dog:
        pass
    
    @abstractmethod
    async def get_all(self, cmd: GetDogsCommand) -> List[Dog]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateDogCommand) -> Dog:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass