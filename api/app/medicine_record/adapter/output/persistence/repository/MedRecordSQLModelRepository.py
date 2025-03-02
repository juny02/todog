from typing import List

from fastapi import Depends
from sqlmodel import Session, col, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.medicine_record.adapter.output.persistence.entities.MedRecordMapper import (
    MedRecordMapper,
)
from app.medicine_record.adapter.output.persistence.entities.MedRecordSQLModelEntity import (
    MedRecordSQLModelEntity,
)
from app.medicine_record.application.error.MedRecordNotFoundError import (
    MedRecordNotFoundError,
)
from app.medicine_record.application.error.MedRecordOwnershipError import MedRecordOwnershipError
from app.medicine_record.application.port.input.CreateMedRecordCommand import (
    CreateMedRecordCommand,
)
from app.medicine_record.application.port.input.GetMedRecordsCommand import GetMedRecordsCommand
from app.medicine_record.application.port.input.UpdateMedRecordCommand import (
    UpdateMedRecordCommand,
)
from app.medicine_record.application.port.output.repository.MedRecordRepository import (
    MedRecordRepository,
)
from app.medicine_record.domain.MedRecord import MedRecord
from app.medicine_schedule.adapter.output.persistence.repository.MedScheduleSQLModelRepository import (
    MedScheduleSQLModelRepository,
)
from app.medicine_schedule.application.error.MedScheduleNotFoundError import (
    MedScheduleNotFoundError,
)
from app.medicine_schedule.application.port.output.repository.MedScheduleRepository import (
    MedScheduleRepository,
)
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.error.UserNotFoundError import UserNotFoundError
from core.db.dependency import get_session
from core.enums import SortOrder


class MedRecordSQLModelRepository(MedRecordRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
        user_repo: DogRepository = Depends(UserSQLModelRepository),
        med_schedule_repo: MedScheduleRepository = Depends(MedScheduleSQLModelRepository)
    ):
        self.mapper = MedRecordMapper
        self.session = session
        self.dog_repo = dog_repo
        self.user_repo = user_repo
        self.med_schedule_repo = med_schedule_repo

    async def create(self, cmd: CreateMedRecordCommand) -> MedRecord:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        if await self.user_repo.get(cmd.user_id) is None:
            raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")
        
        if cmd.schedule_id and await self.med_schedule_repo.get(id=cmd.schedule_id, dog_id=cmd.dog_id) is None:
            raise MedScheduleNotFoundError(f"Med Schedule with id '{cmd.user_id}' does not exist.")

        medicine_record = MedRecordSQLModelEntity(
            dog_id=cmd.dog_id,
            user_id=cmd.user_id,
            given_at=cmd.given_at,
            schedule_id=cmd.schedule_id,
            dose_given=cmd.dose_given,
            photo_url=cmd.photo_url,
            description=cmd.description,
        )

        self.session.add(medicine_record)
        self.session.commit()
        self.session.refresh(medicine_record)

        return self.mapper.map_to_domain(medicine_record)

    async def get(self, id: str, dog_id: str) -> MedRecord:
        medicine_record = await self._get_by_id_for_dog(id=id, dog_id=dog_id)
        return self.mapper.map_to_domain(medicine_record)

    async def get_all(self, cmd: GetMedRecordsCommand) -> List[MedRecord]:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        statement = select(MedRecordSQLModelEntity)
        statement = statement.where(MedRecordSQLModelEntity.dog_id == cmd.dog_id)
        
        if cmd.start:
            statement = statement.where(col(MedRecordSQLModelEntity.given_at) >= cmd.start)
        if cmd.end:
            statement = statement.where(col(MedRecordSQLModelEntity.given_at) <= cmd.end)
        
        if cmd.user_id:
            statement = statement.where(MedRecordSQLModelEntity.user_id == cmd.user_id)
        if cmd.schedule_id:
            statement = statement.where(MedRecordSQLModelEntity.schedule_id == cmd.schedule_id)
        if cmd.given_at:
            statement = statement.where(MedRecordSQLModelEntity.given_at == cmd.given_at)
        if cmd.description:
            statement = statement.where(
                col(MedRecordSQLModelEntity.description).contains(cmd.description)
            )
            
        if cmd.order == SortOrder.DESC:
            statement = statement.order_by(col(MedRecordSQLModelEntity.given_at).desc())
        else:
            statement = statement.order_by(col(MedRecordSQLModelEntity.given_at).asc())


        medicine_records = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(medicine_record) for medicine_record in medicine_records]

    async def update(self, cmd: UpdateMedRecordCommand) -> MedRecord:
        medicine_record = await self._get_by_id_for_dog(id=cmd.id, dog_id=cmd.dog_id)

        if cmd.user_id is not None:
            if await self.user_repo.get(cmd.user_id) is None:
                raise UserNotFoundError(f"User with id '{cmd.user_id}' does not exist.")
            medicine_record.user_id = cmd.user_id
        if cmd.given_at is not None:
            medicine_record.given_at = cmd.given_at
        if cmd.schedule_id is not None:
            if await self.med_schedule_repo.get(id=cmd.schedule_id, dog_id=cmd.dog_id) is None:
                raise MedScheduleNotFoundError(f"Med Schedule with id '{cmd.user_id}' does not exist.")
            medicine_record.schedule_id = cmd.schedule_id
        if cmd.dose_given is not None:
            medicine_record.dose_given = cmd.dose_given
        if cmd.description is not None:
            medicine_record.description = cmd.description
        if cmd.photo_url is not None:
            medicine_record.photo_url = cmd.photo_url

        self.session.commit()
        self.session.refresh(medicine_record)

        return self.mapper.map_to_domain(medicine_record)

    async def delete(self, id: str, dog_id: str) -> None:
        medicine_record = await self._get_by_id_for_dog(id=id, dog_id=dog_id)

        self.session.delete(medicine_record)
        self.session.commit()

    async def _get_by_id(self, id: str) -> MedRecordSQLModelEntity:
        medicine_record = self.session.get(MedRecordSQLModelEntity, id)
        if not medicine_record:
            raise MedRecordNotFoundError(f"MedRecord with ID '{id}' not found")
        return medicine_record

    async def _get_by_id_for_dog(
        self, id: str, dog_id: str
    ) -> MedRecordSQLModelEntity:
        medicine_record = self.session.get(MedRecordSQLModelEntity, id)
        if not medicine_record:
            raise MedRecordNotFoundError(f"MedRecord with ID '{id}' not found")
        if medicine_record.dog_id != dog_id:
            raise MedRecordOwnershipError(
                f"MedRecord {id} does not belong to Dog {dog_id}."
            )

        return medicine_record
