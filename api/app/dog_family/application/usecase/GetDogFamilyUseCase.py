from api.app.dog_family.adapter.output.persistence.repository.DogFamilySQLModelRepository import (
    DogFamilySQLModelRepository,
)
from api.app.dog_family.application.port.output.repository.DogFamilyRepository import (
    DogFamilyRepository,
)
from api.app.dog_family.domain.DogFamily import DogFamily
from fastapi import Depends


class GetDogFamilyUseCase:
    def __init__(self, repo: DogFamilyRepository = Depends(DogFamilySQLModelRepository)):
        self.repo = repo

    async def __call__(self, id: str) -> DogFamily:
        return await self.repo.get(id)