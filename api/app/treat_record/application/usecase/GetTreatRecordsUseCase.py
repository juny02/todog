from typing import List

from fastapi import Depends

from app.treat_record.adapter.output.persistence.repository.TreatRecordSQLModelRepository import (
    TreatRecordSQLModelRepository,
)
from app.treat_record.application.port.input.GetTreatRecordsCommand import GetTreatRecordsCommand
from app.treat_record.application.port.output.repository.TreatRecordRepository import (
    TreatRecordRepository,
)
from app.treat_record.domain.TreatRecord import TreatRecord


class GetTreatRecordsUseCase:
    def __init__(self, treat_record_repo: TreatRecordRepository = Depends(TreatRecordSQLModelRepository)):
        self.treat_record_repo = treat_record_repo
    
    async def __call__(self, cmd: GetTreatRecordsCommand) -> List[TreatRecord]:
        return await self.treat_record_repo.get_all(cmd)