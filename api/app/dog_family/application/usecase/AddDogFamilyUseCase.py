
from fastapi import Depends

from app.dog_family.adapter.output.persistence.repository.DogFamilySQLModelRepository import (
    DogFamilySQLModelRepository,
)
from app.dog_family.application.port.input.AddDogFamilyCommand import AddDogFamilyCommand
from app.dog_family.application.port.output.repository.DogFamilyRepository import (
    DogFamilyRepository,
)
from app.dog_family.domain.DogFamily import DogFamily


class AddDogFamilyUseCase:
    def __init__(self, repo: DogFamilyRepository = Depends(DogFamilySQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, cmd: AddDogFamilyCommand) -> DogFamily:
        return await self.repo.create(cmd)