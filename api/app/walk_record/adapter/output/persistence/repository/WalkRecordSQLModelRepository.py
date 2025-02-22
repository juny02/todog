from typing import List

from fastapi import Depends
from sqlmodel import Session, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository

from app.walk_record.adapter.output.persistence.entities.WalkRecordMapper import (
    WalkRecordMapper,
)
from app.walk_record.adapter.output.persistence.entities.WalkRecordSQLModelEntity import (
    WalkRecordSQLModelEntity,
)
from app.walk_record.application.error.WalkRecordNotFoundError import (
    WalkRecordNotFoundError,
)
from app.walk_record.application.error.WalkRecordOwnershipError import (
    WalkRecordOwnershipError,
)
from app.walk_record.application.port.input.CreateWalkRecordCommand import (
    CreateWalkRecordCommand,
)
from app.walk_record.application.port.input.UpdateWalkRecordCommand import (
    UpdateWalkRecordCommand,
)
from app.walk_record.application.port.output.repository.WalkRecordRepository import (
    WalkRecordRepository,
)
from app.walk_record.domain.WalkRecord import WalkRecord
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.error.UserNotFoundError import UserNotFoundError
from core.db.dependency import get_session


class WalkRecordSQLModelRepository(WalkRecordRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
        user_repo: DogRepository = Depends(UserSQLModelRepository),
    ):
        self.mapper = WalkRecordMapper
        self.session = session
        self.dog_repo = dog_repo
        self.user_repo = user_repo

    async def create(self, cmd: CreateWalkRecordCommand) -> WalkRecord:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        if await self.user_repo.get(cmd.user_id) is None:
            raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")

        walk_record = WalkRecordSQLModelEntity(
            dog_id=cmd.dog_id,
            user_id=cmd.user_id,
            start_time=cmd.start_time,
            end_time=cmd.end_time,
            photo_url=cmd.photo_url,
            description=cmd.description,
        )

        self.session.add(walk_record)
        self.session.commit()
        self.session.refresh(walk_record)

        return self.mapper.map_to_domain(walk_record)

    async def get(self, id: str, dog_id: str) -> WalkRecord:
        walk_record = await self._get_by_id_for_dog(id=id, dog_id=dog_id)
        return self.mapper.map_to_domain(walk_record)

    async def get_all_by_dog(self, dog_id: str) -> List[WalkRecord]:

        if await self.dog_repo.get(dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{dog_id}' does not exist.")

        statement = select(WalkRecordSQLModelEntity)
        statement = statement.where(WalkRecordSQLModelEntity.dog_id == dog_id)

        walk_records = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(walk_record) for walk_record in walk_records]

    async def update(self, cmd: UpdateWalkRecordCommand) -> WalkRecord:
        walk_record = await self._get_by_id_for_dog(id=cmd.id, dog_id=cmd.dog_id)

        if cmd.user_id is not None:
            if await self.user_repo.get(cmd.user_id) is None:
                raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")
            walk_record.user_id = cmd.user_id
        if cmd.start_time is not None:
            walk_record.start_time = cmd.start_time
        if cmd.end_time is not None:
            walk_record.end_time = cmd.end_time
        if cmd.description is not None:
            walk_record.description = cmd.description
        if cmd.photo_url is not None:
            walk_record.photo_url = cmd.photo_url

        self.session.commit()
        self.session.refresh(walk_record)

        return self.mapper.map_to_domain(walk_record)

    async def delete(self, id: str, dog_id: str) -> None:
        walk_record = await self._get_by_id_for_dog(id=id, dog_id=dog_id)

        self.session.delete(walk_record)
        self.session.commit()

    async def _get_by_id(self, id: str) -> WalkRecordSQLModelEntity:
        walk_record = self.session.get(WalkRecordSQLModelEntity, id)
        if not walk_record:
            raise WalkRecordNotFoundError(f"WalkRecord with ID '{id}' not found")
        return walk_record

    async def _get_by_id_for_dog(
        self, id: str, dog_id: str
    ) -> WalkRecordSQLModelEntity:
        walk_record = self.session.get(WalkRecordSQLModelEntity, id)
        if not walk_record:
            raise WalkRecordNotFoundError(f"WalkRecord with ID '{id}' not found")
        if walk_record.dog_id != dog_id:
            raise WalkRecordOwnershipError(
                f"WalkRecord {id} does not belong to Dog {dog_id}."
            )

        return walk_record
