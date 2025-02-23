from fastapi import Depends

from app.memo.adapter.output.persistence.repository.MemoSQLModelRepository import (
    MemoSQLModelRepository,
)
from app.memo.application.port.output.repository.MemoRepository import (
    MemoRepository,
)
from app.memo.domain.Memo import Memo


class GetMemoUseCase:
    def __init__(self, repo: MemoRepository = Depends(MemoSQLModelRepository)):
        self.repo = repo

    async def __call__(self, id: str, dog_id: str) -> Memo:
        return await self.repo.get(id=id, dog_id=dog_id)