from fastapi import Depends

from app.treat.adapter.output.persistence.repository.TreatSQLModelRepository import (
    TreatSQLModelRepository,
)
from app.treat.application.port.output.repository.TreatRepository import TreatRepository
from app.treat.domain.Treat import Treat


class GetTreatUseCase:
    def __init__(self, treat_repo: TreatRepository = Depends(TreatSQLModelRepository)):
        self.treat_repo = treat_repo

    async def __call__(self, id: str, dog_id: str) -> Treat:
        return await self.treat_repo.get(id=id, dog_id=dog_id)
