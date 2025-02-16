from fastapi import Depends

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.port.input.UpdateDogCommand import UpdateDogCommand
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.dog.domain.Dog import Dog


class UpdateDogUseCase:
    def __init__(self, dog_repo: DogRepository = Depends(DogSQLModelRepository)):
        self.dog_repo = dog_repo
    
    async def __call__(self, cmd: UpdateDogCommand) -> Dog:
        return await self.dog_repo.update(cmd)