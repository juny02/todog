from abc import ABC, abstractmethod
from typing import List

from app.medicine_schedule.application.port.input.CreateMedScheduleCommand import (
    CreateMedScheduleCommand,
)
from app.medicine_schedule.application.port.input.GetMedSchedulesCommand import (
    GetMedSchedulesCommand,
)
from app.medicine_schedule.application.port.input.UpdateMedScheduleCommand import (
    UpdateMedScheduleCommand,
)
from app.medicine_schedule.domain.MedSchedule import MedSchedule


class MedScheduleRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateMedScheduleCommand) -> MedSchedule:
        pass

    @abstractmethod
    async def get(self, id: str) -> MedSchedule:
        pass
    
    @abstractmethod
    async def get_all(self, cmd: GetMedSchedulesCommand) -> List[MedSchedule]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateMedScheduleCommand) -> MedSchedule:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass