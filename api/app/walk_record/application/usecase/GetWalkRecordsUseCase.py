from typing import List

from fastapi import Depends

from app.walk_record.adapter.output.persistence.repository.WalkRecordSQLModelRepository import (
    WalkRecordSQLModelRepository,
)
from app.walk_record.application.port.input.GetWalkRecordsCommand import GetWalkRecordsCommand
from app.walk_record.application.port.output.repository.WalkRecordRepository import (
    WalkRecordRepository,
)
from app.walk_record.domain.WalkRecord import WalkRecord


class GetWalkRecordsUseCase:
    def __init__(self, walk_record_repo: WalkRecordRepository = Depends(WalkRecordSQLModelRepository)):
        self.walk_record_repo = walk_record_repo
    
    async def __call__(self, cmd: GetWalkRecordsCommand) -> List[WalkRecord]:
        return await self.walk_record_repo.get_all(cmd)