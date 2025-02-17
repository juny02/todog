from api.app.dog_family.adapter.output.persistence.repository.DogFamilySQLModelRepository import (
    DogFamilySQLModelRepository,
)
from api.app.dog_family.application.port.input.UpdateDogFamilyCommand import UpdateDogFamilyCommand
from api.app.dog_family.application.port.output.repository.DogFamilyRepository import (
    DogFamilyRepository,
)
from fastapi import Depends

from app.dog.domain.Dog import Dog


class UpdateDogFamilyUseCase:
    def __init__(self, repo: DogFamilyRepository = Depends(DogFamilySQLModelRepository)):
        self.repo = repo

    async def __call__(self, cmd: UpdateDogFamilyCommand) -> Dog:
        return await self.repo.update(cmd)