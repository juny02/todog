from fastapi import Depends

from app.medicine_record.adapter.output.persistence.repository.MedRecordSQLModelRepository import (
    MedRecordSQLModelRepository,
)
from app.medicine_record.application.port.output.repository.MedRecordRepository import (
    MedRecordRepository,
)
from app.medicine_record.domain import MedRecord


class DeleteMedRecordUseCase:
    def __init__(self, medicine_record_repo: MedRecordRepository = Depends(MedRecordSQLModelRepository)):
        self.medicine_record_repo = medicine_record_repo
    
    async def __call__(self, id: str, dog_id: str) -> MedRecord:
        return await self.medicine_record_repo.delete(id=id, dog_id=dog_id)