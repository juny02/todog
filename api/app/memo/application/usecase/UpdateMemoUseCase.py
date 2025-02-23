from fastapi import Depends

from app.dog.domain.Dog import Dog
from app.memo.adapter.output.persistence.repository.MemoSQLModelRepository import (
    MemoSQLModelRepository,
)
from app.memo.application.port.input.UpdateMemoCommand import UpdateMemoCommand
from app.memo.application.port.output.repository.MemoRepository import (
    MemoRepository,
)


class UpdateMemoUseCase:
    def __init__(self, repo: MemoRepository = Depends(MemoSQLModelRepository)):
        self.repo = repo

    async def __call__(self, cmd: UpdateMemoCommand) -> Dog:
        return await self.repo.update(cmd)