
from fastapi import Depends

from app.memo.adapter.output.persistence.repository.MemoSQLModelRepository import (
    MemoSQLModelRepository,
)
from app.memo.application.port.input.CreateMemoCommand import CreateMemoCommand
from app.memo.application.port.output.repository.MemoRepository import (
    MemoRepository,
)
from app.memo.domain.Memo import Memo


class CreateMemoUseCase:
    def __init__(self, repo: MemoRepository = Depends(MemoSQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, cmd: CreateMemoCommand) -> Memo:
        return await self.repo.create(cmd)