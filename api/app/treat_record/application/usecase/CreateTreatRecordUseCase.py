
from fastapi import Depends

from app.treat_record.adapter.output.persistence.repository.TreatRecordSQLModelRepository import (
    TreatRecordSQLModelRepository,
)
from app.treat_record.application.port.input.CreateTreatRecordCommand import (
    CreateTreatRecordCommand,
)
from app.treat_record.application.port.output.repository.TreatRecordRepository import (
    TreatRecordRepository,
)
from app.treat_record.domain.TreatRecord import TreatRecord


class CreateTreatRecordUseCase:
    def __init__(self, treat_record_repo: TreatRecordRepository = Depends(TreatRecordSQLModelRepository)):
        self.treat_record_repo = treat_record_repo
    
    async def __call__(self, cmd: CreateTreatRecordCommand) -> TreatRecord:
        return await self.treat_record_repo.create(cmd)