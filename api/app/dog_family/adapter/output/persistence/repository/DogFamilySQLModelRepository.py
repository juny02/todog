from typing import List

from fastapi import Depends
from sqlmodel import Session, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.dog_family.adapter.output.persistence.entities.DogFamilyMapper import (
    DogFamilyMapper,
)
from app.dog_family.adapter.output.persistence.entities.DogFamilySQLModelEntity import (
    DogFamilySQLModelEntity,
)
from app.dog_family.application.error.DogFamilyAlreadyExistsError import (
    DogFamilyAlreadyExistsError,
)
from app.dog_family.application.error.DogFamilyNotFoundError import (
    DogFamilyNotFoundError,
)
from app.dog_family.application.port.input.AddDogFamilyCommand import (
    AddDogFamilyCommand,
)
from app.dog_family.application.port.input.GetDogFamiliesCommand import (
    GetDogFamiliesCommand,
)
from app.dog_family.application.port.input.UpdateDogFamilyCommand import (
    UpdateDogFamilyCommand,
)
from app.dog_family.application.port.output.repository.DogFamilyRepository import (
    DogFamilyRepository,
)
from app.dog_family.domain.DogFamily import DogFamily
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.error.UserNotFoundError import UserNotFoundError
from app.user.application.port.output.repository.UserRepository import (
    UserRepository,
)
from core.db.dependency import get_session


class DogFamilySQLModelRepository(DogFamilyRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
        user_repo: UserRepository = Depends(UserSQLModelRepository),
    ):
        self.mapper = DogFamilyMapper
        self.session = session

        self.dog_repo = dog_repo
        self.user_repo = user_repo

    async def create(self, cmd: AddDogFamilyCommand) -> DogFamily:
        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")
        if await self.user_repo.get(cmd.user_id) is None:
            raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")

        if await self._exists_family(cmd.dog_id, cmd.user_id):
            raise DogFamilyAlreadyExistsError(
                f"DogFamily relationship already exists for dog_id={cmd.dog_id} and user_id={cmd.user_id}"
            )

        dog_family = DogFamilySQLModelEntity(
            dog_id=cmd.dog_id,
            user_id=cmd.user_id,
            user_nickname=cmd.user_nickname,
            dog_nickname=cmd.dog_nickname,
        )

        self.session.add(dog_family)
        self.session.commit()
        self.session.refresh(dog_family)

        return self.mapper.map_to_domain(dog_family)

    async def get(self, id: str) -> DogFamily:
        dog_family = await self._get_by_id(id)
        return self.mapper.map_to_domain(dog_family)

    async def get_all(self, cmd: GetDogFamiliesCommand) -> List[DogFamily]:

        statement = select(DogFamilySQLModelEntity)
        if cmd.dog_id:
            statement = statement.where(DogFamilySQLModelEntity.dog_id == cmd.dog_id)
        if cmd.user_id:
            statement = statement.where(DogFamilySQLModelEntity.user_id == cmd.user_id)
        if cmd.user_nickname:
            statement = statement.where(
                DogFamilySQLModelEntity.user_nickname == cmd.user_nickname
            )
        if cmd.dog_nickname:
            statement = statement.where(
                DogFamilySQLModelEntity.dog_nickname == cmd.dog_nickname
            )

        entities = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(entity) for entity in entities]

    async def update(self, cmd: UpdateDogFamilyCommand) -> DogFamily:
        entity = await self._get_by_id(cmd.id)

        if cmd.dog_id is not None:
            if await self.dog_repo.get(cmd.dog_id) is None:
                raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")
            entity.dog_id = cmd.dog_id
        if await cmd.user_id is not None:
            if self.user_repo.get(cmd.user_id) is None:
                raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")
            entity.user_id = cmd.user_id
        if cmd.user_nickname is not None:
            entity.user_nickname = cmd.user_nickname
        if cmd.dog_nickname is not None:
            entity.dog_nickname = cmd.dog_nickname

        self.session.commit()
        self.session.refresh(entity)

        return self.mapper.map_to_domain(entity)

    async def delete(self, id: str) -> None:
        entity = await self._get_by_id(id)

        self.session.delete(entity)
        self.session.commit()

    async def _get_by_id(self, id: str) -> DogFamilySQLModelEntity:
        entity = self.session.get(DogFamilySQLModelEntity, id)
        if not entity:
            raise DogFamilyNotFoundError(f"DogFamily Relation with ID '{id}' not found")
        return entity

    async def _exists_family(self, dog_id: str, user_id: str) -> bool:
        statement = select(DogFamilySQLModelEntity).where(
            DogFamilySQLModelEntity.dog_id == dog_id,
            DogFamilySQLModelEntity.user_id == user_id,
        )
        return self.session.exec(statement).first() is not None
