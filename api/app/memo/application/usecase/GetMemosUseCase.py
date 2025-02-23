from typing import List

from fastapi import Depends

from app.memo.adapter.output.persistence.repository.MemoSQLModelRepository import (
    MemoSQLModelRepository,
)
from app.memo.application.port.input.GetMemosCommand import GetMemosCommand
from app.memo.application.port.output.repository.MemoRepository import (
    MemoRepository,
)
from app.memo.domain.Memo import Memo


class GetMemosUseCase:
    def __init__(self, repo: MemoRepository = Depends(MemoSQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, cmd: GetMemosCommand) -> List[Memo]:
        return await self.repo.get_all(cmd)