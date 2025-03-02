
from fastapi import Depends

from app.medicine_schedule.adapter.output.persistence.repository.MedScheduleSQLModelRepository import (
    MedScheduleSQLModelRepository,
)
from app.medicine_schedule.application.port.input.CreateMedScheduleCommand import (
    CreateMedScheduleCommand,
)
from app.medicine_schedule.application.port.output.repository.MedScheduleRepository import (
    MedScheduleRepository,
)
from app.medicine_schedule.domain.MedSchedule import MedSchedule


class CreateMedScheduleUseCase:
    def __init__(self, repo: MedScheduleRepository = Depends(MedScheduleSQLModelRepository)):
        self.repo = repo
    
    async def __call__(self, cmd: CreateMedScheduleCommand) -> MedSchedule:
        return await self.repo.create(cmd)