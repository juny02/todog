from fastapi import Depends

from app.memo.adapter.output.persistence.repository.MemoSQLModelRepository import (
    MemoSQLModelRepository,
)
from app.memo.application.port.output.repository.MemoRepository import (
    MemoRepository,
)
from app.memo.domain import Memo


class DeleteMemoUseCase:
    def __init__(self, repo: MemoRepository = Depends(MemoSQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, id: str, dog_id: str) -> Memo:
        return await self.repo.delete(id=id, dog_id=dog_id)