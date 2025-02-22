from fastapi import Depends

from app.treat.adapter.output.persistence.repository.TreatSQLModelRepository import (
    TreatSQLModelRepository,
)
from app.treat.application.port.input.UpdateTreatCommand import UpdateTreatCommand
from app.treat.application.port.output.repository.TreatRepository import TreatRepository
from app.treat.domain.Treat import Treat


class UpdateTreatUseCase:
    def __init__(self, treat_repo: TreatRepository = Depends(TreatSQLModelRepository)):
        self.treat_repo = treat_repo
    
    async def __call__(self, cmd: UpdateTreatCommand) -> Treat:
        return await self.treat_repo.update(cmd)