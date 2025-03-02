from typing import List

from fastapi import Depends

from app.medicine_schedule.adapter.output.persistence.repository.MedScheduleSQLModelRepository import (
    MedScheduleSQLModelRepository,
)
from app.medicine_schedule.application.port.input.GetMedSchedulesCommand import (
    GetMedSchedulesCommand,
)
from app.medicine_schedule.application.port.output.repository.MedScheduleRepository import (
    MedScheduleRepository,
)
from app.medicine_schedule.domain.MedSchedule import MedSchedule


class GetMedSchedulesUseCase:
    def __init__(self, repo: MedScheduleRepository = Depends(MedScheduleSQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, cmd: GetMedSchedulesCommand) -> List[MedSchedule]:
        return await self.repo.get_all(cmd)