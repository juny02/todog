from abc import ABC, abstractmethod
from typing import List

from app.schedule.application.port.input.CreateScheduleCommand import CreateScheduleCommand
from app.schedule.application.port.input.GetSchedulesCommand import GetSchedulesCommand
from app.schedule.application.port.input.UpdateScheduleCommand import UpdateScheduleCommand
from app.schedule.domain.Schedule import Schedule


class ScheduleRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateScheduleCommand) -> Schedule:
        pass

    @abstractmethod
    async def get(self, id: str) -> Schedule:
        pass
    
    @abstractmethod
    async def get_all(self, cmd: GetSchedulesCommand) -> List[Schedule]:
        pass


    @abstractmethod
    async def update(self, cmd: UpdateScheduleCommand) -> Schedule:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass