from abc import ABC, abstractmethod
from typing import List

from app.memo.application.port.input.CreateMemoCommand import CreateMemoCommand
from app.memo.application.port.input.GetMemosCommand import GetMemosCommand
from app.memo.application.port.input.UpdateMemoCommand import UpdateMemoCommand
from app.memo.domain.Memo import Memo


class MemoRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateMemoCommand) -> Memo:
        pass

    @abstractmethod
    async def get(self, id: str) -> Memo:
        pass
    
    @abstractmethod
    async def get_all(self, cmd: GetMemosCommand) -> List[Memo]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateMemoCommand) -> Memo:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass