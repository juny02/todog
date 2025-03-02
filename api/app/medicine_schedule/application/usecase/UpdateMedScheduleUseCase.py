from fastapi import Depends

from app.dog.domain.Dog import Dog
from app.medicine_schedule.adapter.output.persistence.repository.MedScheduleSQLModelRepository import (
    MedScheduleSQLModelRepository,
)
from app.medicine_schedule.application.port.input.UpdateMedScheduleCommand import (
    UpdateMedScheduleCommand,
)
from app.medicine_schedule.application.port.output.repository.MedScheduleRepository import (
    MedScheduleRepository,
)


class UpdateMedScheduleUseCase:
    def __init__(self, repo: MedScheduleRepository = Depends(MedScheduleSQLModelRepository)):
        self.repo = repo

    async def __call__(self, cmd: UpdateMedScheduleCommand) -> Dog:
        return await self.repo.update(cmd)