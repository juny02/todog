from typing import List

from fastapi import Depends
from sqlmodel import Session, col, select

from app.dog.adapter.output.persistence.repository.DogSQLModelRepository import (
    DogSQLModelRepository,
)
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.output.repository.DogRepository import DogRepository
from app.schedule.adapter.output.persistence.entities.ScheduleMapper import (
    ScheduleMapper,
)
from app.schedule.adapter.output.persistence.entities.ScheduleSQLModelEntity import (
    ScheduleSQLModelEntity,
)
from app.schedule.application.error.ScheduleNotFoundError import (
    ScheduleNotFoundError,
)
from app.schedule.application.error.ScheduleOwnershipError import (
    ScheduleOwnershipError,
)
from app.schedule.application.port.input.CreateScheduleCommand import (
    CreateScheduleCommand,
)
from app.schedule.application.port.input.GetSchedulesCommand import GetSchedulesCommand
from app.schedule.application.port.input.UpdateScheduleCommand import (
    UpdateScheduleCommand,
)
from app.schedule.application.port.output.repository.ScheduleRepository import (
    ScheduleRepository,
)
from app.schedule.domain.Schedule import Schedule
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from core.db.dependency import get_session
from core.enums import SortOrder


class ScheduleSQLModelRepository(ScheduleRepository):

    def __init__(
        self,
        session: Session = Depends(get_session),
        dog_repo: DogRepository = Depends(DogSQLModelRepository),
        user_repo: DogRepository = Depends(UserSQLModelRepository),
    ):
        self.mapper = ScheduleMapper
        self.session = session
        self.dog_repo = dog_repo
        self.user_repo = user_repo

    async def create(self, cmd: CreateScheduleCommand) -> Schedule:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        schedule = ScheduleSQLModelEntity(
            dog_id=cmd.dog_id,
            title=cmd.title,
            content=cmd.content,
            complete=cmd.complete,
            scheduled_at=cmd.scheduled_at,
        )

        self.session.add(schedule)
        self.session.commit()
        self.session.refresh(schedule)

        return self.mapper.map_to_domain(schedule)

    async def get(self, id: str, dog_id: str) -> Schedule:
        schedule = await self._get_by_id_for_dog(id=id, dog_id=dog_id)
        return self.mapper.map_to_domain(schedule)

    async def get_all(self, cmd: GetSchedulesCommand) -> List[Schedule]:

        if await self.dog_repo.get(cmd.dog_id) is None:
            raise DogNotFoundError(f"Dog with id '{cmd.dog_id}' does not exist.")

        statement = select(ScheduleSQLModelEntity)
        statement = statement.where(ScheduleSQLModelEntity.dog_id == cmd.dog_id)

        if cmd.start:
            statement = statement.where(
                col(ScheduleSQLModelEntity.scheduled_at) >= cmd.start
            )
        if cmd.end:
            statement = statement.where(
                col(ScheduleSQLModelEntity.scheduled_at) <= cmd.end
            )

        if cmd.scheduled_at:
            statement = statement.where(
                ScheduleSQLModelEntity.scheduled_at == cmd.scheduled_at
            )
        if cmd.complete:
            statement = statement.where(ScheduleSQLModelEntity.complete == cmd.complete)
        if cmd.title:
            statement = statement.where(
                col(ScheduleSQLModelEntity.title).contains(cmd.title)
            )
        if cmd.content:
            statement = statement.where(
                col(ScheduleSQLModelEntity.content).contains(cmd.content)
            )

        if cmd.order == SortOrder.DESC:
            statement = statement.order_by(
                col(ScheduleSQLModelEntity.scheduled_at).desc()
            )
        else:
            statement = statement.order_by(col(ScheduleSQLModelEntity.scheduled_at).asc())

        schedules = self.session.exec(statement).all()

        return [self.mapper.map_to_domain(schedule) for schedule in schedules]

    async def update(self, cmd: UpdateScheduleCommand) -> Schedule:
        schedule = await self._get_by_id_for_dog(id=cmd.id, dog_id=cmd.dog_id)

        if cmd.title is not None:
            schedule.title = cmd.title
        if cmd.content is not None:
            schedule.content = cmd.content
        if cmd.complete is not None:
            schedule.complete = cmd.complete
        if cmd.scheduled_at is not None:
            schedule.scheduled_at = cmd.scheduled_at

        self.session.commit()
        self.session.refresh(schedule)

        return self.mapper.map_to_domain(schedule)

    async def delete(self, id: str, dog_id: str) -> None:
        schedule = await self._get_by_id_for_dog(id=id, dog_id=dog_id)

        self.session.delete(schedule)
        self.session.commit()

    async def _get_by_id(self, id: str) -> ScheduleSQLModelEntity:
        schedule = self.session.get(ScheduleSQLModelEntity, id)
        if not schedule:
            raise ScheduleNotFoundError(f"Schedule with ID '{id}' not found")
        return schedule

    async def _get_by_id_for_dog(self, id: str, dog_id: str) -> ScheduleSQLModelEntity:
        schedule = self.session.get(ScheduleSQLModelEntity, id)
        if not schedule:
            raise ScheduleNotFoundError(f"Schedule with ID '{id}' not found")
        if schedule.dog_id != dog_id:
            raise ScheduleOwnershipError(
                f"Schedule {id} does not belong to Dog {dog_id}."
            )

        return schedule
