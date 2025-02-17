from fastapi import Depends

from app.user.domain.User import User
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.port.input.UpdateUserCommand import UpdateUserCommand
from app.user.application.port.output.repository.UserRepository import UserRepository


class UpdateUserUseCase:
    def __init__(self, user_repo: UserRepository = Depends(UserSQLModelRepository)):
        self.user_repo = user_repo
    
    async def __call__(self, cmd: UpdateUserCommand) -> User:
        return await self.user_repo.update(cmd)