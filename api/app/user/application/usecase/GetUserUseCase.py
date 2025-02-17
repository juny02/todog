from fastapi import Depends

from app.dog.domain.Dog import Dog
from app.user.adapter.output.persistence.repository.UserSQLModelRepository import (
    UserSQLModelRepository,
)
from app.user.application.port.output.repository.UserRepository import UserRepository


class GetUserUseCase:
    def __init__(self, user_repo: UserRepository = Depends(UserSQLModelRepository)):
        self.user_repo = user_repo
    
    async def __call__(self, id: str) -> Dog:
        return await self.user_repo.get(id)