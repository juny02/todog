from fastapi import Depends

from app.feature.auth.adapter.output.persistence import AlchemyUserRepository
from app.feature.auth.domain import User, UserStatus


class DisableUserUseCase:
    def __init__(
        self,
        user_repo: AlchemyUserRepository = Depends(),
    ):
        self.user_repo = user_repo

    async def __call__(self, user_id: str) -> User:
        user = await self.user_repo.get_by_id(user_id)
        user.status = UserStatus.INACTIVE

        return await self.user_repo.update(user)
