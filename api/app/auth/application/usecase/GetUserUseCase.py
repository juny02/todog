from fastapi import Depends

from app.feature.auth.adapter.output.persistence import AlchemyUserRepository
from app.feature.auth.domain import User


class GetUserUseCase:
    def __init__(
        self,
        user_repo: AlchemyUserRepository = Depends(),
    ):
        self.user_repo = user_repo

    async def __call__(self, user_id: str) -> User:
        return await self.user_repo.get_by_id(user_id)
