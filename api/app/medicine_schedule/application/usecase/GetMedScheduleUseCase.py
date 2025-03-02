from fastapi import Depends

from app.medicine_schedule.adapter.output.persistence.repository.MedScheduleSQLModelRepository import (
    MedScheduleSQLModelRepository,
)
from app.medicine_schedule.application.port.output.repository.MedScheduleRepository import (
    MedScheduleRepository,
)
from app.medicine_schedule.domain.MedSchedule import MedSchedule


class GetMedScheduleUseCase:
    def __init__(self, repo: MedScheduleRepository = Depends(MedScheduleSQLModelRepository)):
        self.repo = repo

    async def __call__(self, id: str, dog_id: str) -> MedSchedule:
        return await self.repo.get(id=id, dog_id=dog_id)
    