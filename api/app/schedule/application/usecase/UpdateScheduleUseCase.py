from fastapi import Depends

from app.dog.domain.Dog import Dog
from app.schedule.adapter.output.persistence.repository.ScheduleSQLModelRepository import (
    ScheduleSQLModelRepository,
)
from app.schedule.application.port.input.UpdateScheduleCommand import UpdateScheduleCommand
from app.schedule.application.port.output.repository.ScheduleRepository import (
    ScheduleRepository,
)


class UpdateScheduleUseCase:
    def __init__(self, repo: ScheduleRepository = Depends(ScheduleSQLModelRepository)):
        self.repo = repo

    async def __call__(self, cmd: UpdateScheduleCommand) -> Dog:
        return await self.repo.update(cmd)