from fastapi import Depends

from app.schedule.adapter.output.persistence.repository.ScheduleSQLModelRepository import (
    ScheduleSQLModelRepository,
)
from app.schedule.application.port.output.repository.ScheduleRepository import (
    ScheduleRepository,
)
from app.schedule.domain.Schedule import Schedule


class GetScheduleUseCase:
    def __init__(self, repo: ScheduleRepository = Depends(ScheduleSQLModelRepository)):
        self.repo = repo

    async def __call__(self, id: str, dog_id: str) -> Schedule:
        return await self.repo.get(id=id, dog_id=dog_id)