from typing import List

from fastapi import Depends
from sqlmodel import Session, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.treat.adapter.output.persistence.repository.TreatSQLModelRepository import (
    TreatSQLModelRepository,
)
from app.treat.application.error.TreatNotFoundError import TreatNotFoundError
from app.treat_record.adapter.output.persistence.entities.TreatRecordMapper import (
    TreatRecordMapper,
)
from app.treat_record.adapter.output.persistence.entities.TreatRecordSQLModelEntity import (
    TreatRecordSQLModelEntity,
)
from app.treat_record.application.error.TreatRecordNotFoundError import (
    TreatRecordNotFoundError,
)
from app.treat_record.application.error.TreatRecordOwnershipError import (
    TreatRecordOwnershipError,
)
from app.treat_record.application.port.input.CreateTreatRecordCommand import (
    CreateTreatRecordCommand,
)
from app.treat_record.application.port.input.UpdateTreatRecordCommand import (
    UpdateTreatRecordCommand,
)
from app.treat_record.application.port.output.repository.TreatRecordRepository import (
    TreatRecordRepository,
)
from app.treat_record.domain.TreatRecord import TreatRecord
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.error.UserNotFoundError import UserNotFoundError
from core.db.dependency import get_session


class TreatRecordSQLModelRepository(TreatRecordRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
        treat_repo: DogRepository = Depends(TreatSQLModelRepository),
        user_repo: DogRepository = Depends(UserSQLModelRepository),
    ):
        self.mapper = TreatRecordMapper
        self.session = session
        self.dog_repo = dog_repo
        self.treat_repo = treat_repo
        self.user_repo = user_repo

    async def create(self, cmd: CreateTreatRecordCommand) -> TreatRecord:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        if await self.user_repo.get(cmd.user_id) is None:
            raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")

        if await self.treat_repo.get(id=cmd.treat_id, dog_id=cmd.dog_id) is None:
            raise TreatNotFoundError(f"Treat with id '{cmd.treat_id}' does not exist.")

        treat_record = TreatRecordSQLModelEntity(
            dog_id=cmd.dog_id,
            user_id=cmd.user_id,
            treat_id=cmd.treat_id,
            quantity=cmd.quantity,
            given_at=cmd.given_at,
            description=cmd.description,
            photo_url=cmd.photo_url,
        )

        self.session.add(treat_record)
        self.session.commit()
        self.session.refresh(treat_record)

        return self.mapper.map_to_domain(treat_record)

    async def get(self, id: str, dog_id: str) -> TreatRecord:
        treat_record = await self._get_by_id_for_dog(id=id, dog_id=dog_id)
        return self.mapper.map_to_domain(treat_record)

    async def get_all_by_dog(self, dog_id: str) -> List[TreatRecord]:

        if await self.dog_repo.get(dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{dog_id}' does not exist.")

        statement = select(TreatRecordSQLModelEntity)
        statement = statement.where(TreatRecordSQLModelEntity.dog_id == dog_id)

        treat_records = self.session.exec(statement).all()

        return [
            self.mapper.map_to_domain(treat_record) for treat_record in treat_records
        ]

    async def update(self, cmd: UpdateTreatRecordCommand) -> TreatRecord:
        treat_record = await self._get_by_id_for_dog(id=cmd.id, dog_id=cmd.dog_id)

        if cmd.user_id is not None:
            if await self.user_repo.get(cmd.user_id) is None:
                raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")
            treat_record.user_id = cmd.user_id
        if cmd.treat_id is not None:
            if await self.treat_repo.get(id=cmd.treat_id, dog_id=cmd.dog_id) is None:
                raise TreatNotFoundError(
                    f"Treat with id '{cmd.treat_id}' does not exist."
                )
            treat_record.treat_id = cmd.treat_id
        if cmd.quantity is not None:
            treat_record.quantity = cmd.quantity
        if cmd.given_at is not None:
            treat_record.given_at = cmd.given_at
        if cmd.description is not None:
            treat_record.description = cmd.description
        if cmd.photo_url is not None:
            treat_record.photo_url = cmd.photo_url


        self.session.commit()
        self.session.refresh(treat_record)

        return self.mapper.map_to_domain(treat_record)

    async def delete(self, id: str, dog_id: str) -> None:
        treat_record = await self._get_by_id_for_dog(id=id, dog_id=dog_id)

        self.session.delete(treat_record)
        self.session.commit()

    async def _get_by_id(self, id: str) -> TreatRecordSQLModelEntity:
        treat_record = self.session.get(TreatRecordSQLModelEntity, id)
        if not treat_record:
            raise TreatRecordNotFoundError(f"TreatRecord with ID '{id}' not found")
        return treat_record

    async def _get_by_id_for_dog(
        self, id: str, dog_id: str
    ) -> TreatRecordSQLModelEntity:
        treat_record = self.session.get(TreatRecordSQLModelEntity, id)
        if not treat_record:
            raise TreatRecordNotFoundError(f"TreatRecord with ID '{id}' not found")
        if treat_record.dog_id != dog_id:
            raise TreatRecordOwnershipError(
                f"TreatRecord {id} does not belong to Dog {dog_id}."
            )

        return treat_record
