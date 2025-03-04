from fastapi import Depends

from app.feature.auth.adapter.output.persistence import AlchemyUserRepository
from app.feature.auth.application.port.input import SearchUsersCommand
from app.feature.auth.domain import User
from app.feature.shared.pagination.domain.model import Page


class SearchUserUseCase:
    def __init__(
        self,
        user_repo: AlchemyUserRepository = Depends(),
    ):
        self.user_repo = user_repo

    async def __call__(self, cmd: SearchUsersCommand) -> Page[User]:
        return await self.user_repo.search(cmd)
