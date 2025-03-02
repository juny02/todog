from typing import List

from fastapi import Depends
from sqlmodel import Session, col, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.medicine_schedule.adapter.output.persistence.entities.MedScheduleMapper import (
    MedScheduleMapper,
)
from app.medicine_schedule.adapter.output.persistence.entities.MedScheduleSQLModelEntity import (
    MedScheduleSQLModelEntity,
)
from app.medicine_schedule.application.error.MedScheduleNotFoundError import (
    MedScheduleNotFoundError,
)
from app.medicine_schedule.application.error.MedScheduleOwnershipError import (
    MedScheduleOwnershipError,
)
from app.medicine_schedule.application.port.input.CreateMedScheduleCommand import (
    CreateMedScheduleCommand,
)
from app.medicine_schedule.application.port.input.GetMedSchedulesCommand import (
    GetMedSchedulesCommand,
)
from app.medicine_schedule.application.port.input.UpdateMedScheduleCommand import (
    UpdateMedScheduleCommand,
)
from app.medicine_schedule.application.port.output.repository.MedScheduleRepository import (
    MedScheduleRepository,
)
from app.medicine_schedule.domain.MedSchedule import MedSchedule
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from core.db.dependency import get_session
from core.enums import SortOrder


class MedScheduleSQLModelRepository(MedScheduleRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
        user_repo: DogRepository = Depends(UserSQLModelRepository),
    ):
        self.mapper = MedScheduleMapper
        self.session = session
        self.dog_repo = dog_repo
        self.user_repo = user_repo

    async def create(self, cmd: CreateMedScheduleCommand) -> MedSchedule:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        medicine_schedule = MedScheduleSQLModelEntity(
            dog_id=cmd.dog_id,
            medicine_name=cmd.medicine_name,
            dosage=cmd.dosage,
            daily_doses=cmd.daily_doses,
            dose_times=cmd.dose_times,
            type=cmd.type,
            interval_days=cmd.interval_days,
            start=cmd.start,
            end=cmd.end,
            notes=cmd.notes
        )

        self.session.add(medicine_schedule)
        self.session.commit()
        self.session.refresh(medicine_schedule)

        return self.mapper.map_to_domain(medicine_schedule)

    async def get(self, id: str, dog_id: str) -> MedSchedule:
        medicine_schedule = await self._get_by_id_for_dog(id=id, dog_id=dog_id)
        return self.mapper.map_to_domain(medicine_schedule)

    async def get_all(self, cmd: GetMedSchedulesCommand) -> List[MedSchedule]:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        statement = select(MedScheduleSQLModelEntity)
        statement = statement.where(MedScheduleSQLModelEntity.dog_id == cmd.dog_id)
        if cmd.start:
            statement = statement.where(
                col(MedScheduleSQLModelEntity.start) >= cmd.start
            )
        if cmd.end:
            statement = statement.where(
                col(MedScheduleSQLModelEntity.start) <= cmd.end
            )
        if cmd.date:
            statement = statement.where(
                col(MedScheduleSQLModelEntity.start) <= cmd.date <= col(MedScheduleSQLModelEntity.end)
            )
        if cmd.daily_doses:
            statement = statement.where(
                MedScheduleSQLModelEntity.daily_doses == cmd.daily_doses
            )
        if cmd.dosage:
            statement = statement.where(MedScheduleSQLModelEntity.dosage == cmd.dosage)
        if cmd.type:
            statement = statement.where(MedScheduleSQLModelEntity.type == cmd.type)
        if cmd.interval_days:
            statement = statement.where(MedScheduleSQLModelEntity.interval_days == cmd.interval_days)
        if cmd.medicine_name:
            statement = statement.where(
                col(MedScheduleSQLModelEntity.medicine_name).contains(cmd.medicine_name)
            )

        if cmd.order == SortOrder.DESC:
            statement = statement.order_by(
                col(MedScheduleSQLModelEntity.start).desc()
            )
        else:
            statement = statement.order_by(col(MedScheduleSQLModelEntity.start).asc())

        medicine_schedules = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(medicine_schedule) for medicine_schedule in medicine_schedules]

    async def update(self, cmd: UpdateMedScheduleCommand) -> MedSchedule:
        medicine_schedule = await self._get_by_id_for_dog(id=cmd.id, dog_id=cmd.dog_id)

        if cmd.medicine_name is not None:
            medicine_schedule.medicine_name = cmd.medicine_name
        if cmd.dosage is not None:
            medicine_schedule.dosage = cmd.dosage
        if cmd.type is not None:
            medicine_schedule.type = cmd.type
        if cmd.interval_days is not None:
            medicine_schedule.interval_days = cmd.interval_days
        if cmd.start is not None:
            medicine_schedule.start = cmd.start
        if cmd.end is not None:
            medicine_schedule.end = cmd.end
        if cmd.notes is not None:
            medicine_schedule.notes = cmd.notes

        self.session.commit()
        self.session.refresh(medicine_schedule)

        return self.mapper.map_to_domain(medicine_schedule)

    async def delete(self, id: str, dog_id: str) -> None:
        medicine_schedule = await self._get_by_id_for_dog(id=id, dog_id=dog_id)

        self.session.delete(medicine_schedule)
        self.session.commit()

    async def _get_by_id(self, id: str) -> MedScheduleSQLModelEntity:
        medicine_schedule = self.session.get(MedScheduleSQLModelEntity, id)
        if not medicine_schedule:
            raise MedScheduleNotFoundError(f"MedSchedule with ID '{id}' not found")
        return medicine_schedule

    async def _get_by_id_for_dog(self, id: str, dog_id: str) -> MedScheduleSQLModelEntity:
        medicine_schedule = self.session.get(MedScheduleSQLModelEntity, id)
        if not medicine_schedule:
            raise MedScheduleNotFoundError(f"MedSchedule with ID '{id}' not found")
        if medicine_schedule.dog_id != dog_id:
            raise MedScheduleOwnershipError(
                f"MedSchedule {id} does not belong to Dog {dog_id}."
            )

        return medicine_schedule
