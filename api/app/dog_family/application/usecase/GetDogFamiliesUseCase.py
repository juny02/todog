from typing import List

from fastapi import Depends

from app.dog_family.adapter.output.persistence.repository.DogFamilySQLModelRepository import (
    DogFamilySQLModelRepository,
)
from app.dog_family.application.port.input.GetDogFamiliesCommand import GetDogFamiliesCommand
from app.dog_family.application.port.output.repository.DogFamilyRepository import (
    DogFamilyRepository,
)
from app.dog_family.domain.DogFamily import DogFamily


class GetDogFamiliesUseCase:
    def __init__(self, repo: DogFamilyRepository = Depends(DogFamilySQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, cmd: GetDogFamiliesCommand) -> List[DogFamily]:
        return await self.repo.get_all(cmd)