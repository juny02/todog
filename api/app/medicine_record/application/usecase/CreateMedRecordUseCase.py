
from fastapi import Depends

from app.medicine_record.adapter.output.persistence.repository.MedRecordSQLModelRepository import (
    MedRecordSQLModelRepository,
)
from app.medicine_record.application.port.input.CreateMedRecordCommand import (
    CreateMedRecordCommand,
)
from app.medicine_record.application.port.output.repository.MedRecordRepository import (
    MedRecordRepository,
)
from app.medicine_record.domain.MedRecord import MedRecord


class CreateMedRecordUseCase:
    def __init__(self, medicine_record_repo: MedRecordRepository = Depends(MedRecordSQLModelRepository)):
        self.medicine_record_repo = medicine_record_repo
    
    async def __call__(self, cmd: CreateMedRecordCommand) -> MedRecord:
        return await self.medicine_record_repo.create(cmd)