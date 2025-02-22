from fastapi import Depends

from app.treat.adapter.output.persistence.repository.TreatSQLModelRepository import (
    TreatSQLModelRepository,
)
from app.treat.application.port.output.repository.TreatRepository import TreatRepository
from app.treat.domain import Treat


class DeleteTreatUseCase:
    def __init__(self, treat_repo: TreatRepository = Depends(TreatSQLModelRepository)):
        self.treat_repo = treat_repo
    
    async def __call__(self, id: str) -> Treat:
        return await self.treat_repo.delete(id)