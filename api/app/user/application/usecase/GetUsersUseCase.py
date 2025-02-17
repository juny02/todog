from typing import List

from fastapi import Depends

from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.port.input.GetUsersCommand import GetUsersCommand
from app.user.application.port.output.repository.UserRepository import UserRepository
from app.user.domain.User import User


class GetUsersUseCase:
    def __init__(self, user_repo: UserRepository = Depends(UserSQLModelRepository)):
        self.user_repo = user_repo
    
    async def __call__(self, cmd: GetUsersCommand) -> List[User]:
        return await self.user_repo.get_all(cmd)