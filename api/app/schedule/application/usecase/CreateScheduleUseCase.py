
from fastapi import Depends

from app.schedule.adapter.output.persistence.repository.ScheduleSQLModelRepository import (
    ScheduleSQLModelRepository,
)
from app.schedule.application.port.input.CreateScheduleCommand import CreateScheduleCommand
from app.schedule.application.port.output.repository.ScheduleRepository import (
    ScheduleRepository,
)
from app.schedule.domain.Schedule import Schedule


class CreateScheduleUseCase:
    def __init__(self, repo: ScheduleRepository = Depends(ScheduleSQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, cmd: CreateScheduleCommand) -> Schedule:
        return await self.repo.create(cmd)