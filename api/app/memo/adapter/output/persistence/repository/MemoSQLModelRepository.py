from typing import List

from fastapi import Depends
from sqlmodel import Session, col, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.memo.adapter.output.persistence.entities.MemoMapper import (
    MemoMapper,
)
from app.memo.adapter.output.persistence.entities.MemoSQLModelEntity import (
    MemoSQLModelEntity,
)
from app.memo.application.error.MemoNotFoundError import (
    MemoNotFoundError,
)
from app.memo.application.error.MemoOwnershipError import (
    MemoOwnershipError,
)
from app.memo.application.port.input.CreateMemoCommand import (
    CreateMemoCommand,
)
from app.memo.application.port.input.GetMemosCommand import GetMemosCommand
from app.memo.application.port.input.UpdateMemoCommand import (
    UpdateMemoCommand,
)
from app.memo.application.port.output.repository.MemoRepository import (
    MemoRepository,
)
from app.memo.domain.Memo import Memo
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.error.UserNotFoundError import UserNotFoundError
from core.db.dependency import get_session
from core.enums import SortOrder


class MemoSQLModelRepository(MemoRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
        user_repo: DogRepository = Depends(UserSQLModelRepository),
    ):
        self.mapper = MemoMapper
        self.session = session
        self.dog_repo = dog_repo
        self.user_repo = user_repo

    async def create(self, cmd: CreateMemoCommand) -> Memo:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        if await self.user_repo.get(cmd.user_id) is None:
            raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")

        memo = MemoSQLModelEntity(
            dog_id=cmd.dog_id,
            user_id=cmd.user_id,
            content=cmd.content,
            created_at=cmd.created_at,
            fixed=cmd.fixed,
        )

        self.session.add(memo)
        self.session.commit()
        self.session.refresh(memo)

        return self.mapper.map_to_domain(memo)

    async def get(self, id: str, dog_id: str) -> Memo:
        memo = await self._get_by_id_for_dog(id=id, dog_id=dog_id)
        return self.mapper.map_to_domain(memo)

    async def get_all(self, cmd: GetMemosCommand) -> List[Memo]:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        statement = select(MemoSQLModelEntity)
        statement = statement.where(MemoSQLModelEntity.dog_id == cmd.dog_id)
        
        if cmd.start:
            statement = statement.where(col(MemoSQLModelEntity.created_at) >= cmd.start)
        if cmd.end:
            statement = statement.where(col(MemoSQLModelEntity.created_at) <= cmd.end)

        if cmd.user_id:
            statement = statement.where(MemoSQLModelEntity.user_id == cmd.user_id)
        if cmd.fixed:
            statement = statement.where(MemoSQLModelEntity.fixed == cmd.fixed)
        if cmd.content:
            statement = statement.where(
                col(MemoSQLModelEntity.content).contains(cmd.content)
            )

        if cmd.order == SortOrder.DESC:
            statement = statement.order_by(col(MemoSQLModelEntity.created_at).desc())
        else:
            statement = statement.order_by(col(MemoSQLModelEntity.created_at).asc())

        memos = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(memo) for memo in memos]

    async def update(self, cmd: UpdateMemoCommand) -> Memo:
        memo = await self._get_by_id_for_dog(id=cmd.id, dog_id=cmd.dog_id)

        if cmd.user_id is not None:
            if await self.user_repo.get(cmd.user_id) is None:
                raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")
            memo.user_id = cmd.user_id
        if cmd.content is not None:
            memo.content = cmd.content
        if cmd.created_at is not None:
            memo.created_at = cmd.created_at
        if cmd.fixed is not None:
            memo.fixed = cmd.fixed

        self.session.commit()
        self.session.refresh(memo)

        return self.mapper.map_to_domain(memo)

    async def delete(self, id: str, dog_id: str) -> None:
        memo = await self._get_by_id_for_dog(id=id, dog_id=dog_id)

        self.session.delete(memo)
        self.session.commit()

    async def _get_by_id(self, id: str) -> MemoSQLModelEntity:
        memo = self.session.get(MemoSQLModelEntity, id)
        if not memo:
            raise MemoNotFoundError(f"Memo with ID '{id}' not found")
        return memo

    async def _get_by_id_for_dog(self, id: str, dog_id: str) -> MemoSQLModelEntity:
        memo = self.session.get(MemoSQLModelEntity, id)
        if not memo:
            raise MemoNotFoundError(f"Memo with ID '{id}' not found")
        if memo.dog_id != dog_id:
            raise MemoOwnershipError(f"Memo {id} does not belong to Dog {dog_id}.")

        return memo
