from fastapi import Depends

from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.port.output.repository.UserRepository import UserRepository
from app.user.domain.User import User


class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepository = Depends(UserSQLModelRepository)):
        self.user_repo = user_repo
    
    async def __call__(self, id: str) -> User:
        return await self.user_repo.delete(id)