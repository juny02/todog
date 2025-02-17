from abc import ABC, abstractmethod
from typing import List

from app.user.application.port.input.CreateUserCommand import CreateUserCommand
from app.user.application.port.input.GetUsersCommand import GetUsersCommand
from app.user.application.port.input.UpdateUserCommand import UpdateUserCommand
from app.user.domain.User import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, cmd: CreateUserCommand) -> User:
        pass

    @abstractmethod
    async def get(self, id: str) -> User:
        pass

    @abstractmethod
    async def get_all(self, cmd: GetUsersCommand) -> List[User]:
        pass

    @abstractmethod
    async def update(self, cmd: UpdateUserCommand) -> User:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass
