from typing import List

from fastapi import Depends

from app.schedule.adapter.output.persistence.repository.ScheduleSQLModelRepository import (
    ScheduleSQLModelRepository,
)
from app.schedule.application.port.input.GetSchedulesCommand import GetSchedulesCommand
from app.schedule.application.port.output.repository.ScheduleRepository import (
    ScheduleRepository,
)
from app.schedule.domain.Schedule import Schedule


class GetSchedulesUseCase:
    def __init__(self, repo: ScheduleRepository = Depends(ScheduleSQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, cmd: GetSchedulesCommand) -> List[Schedule]:
        return await self.repo.get_all(cmd)