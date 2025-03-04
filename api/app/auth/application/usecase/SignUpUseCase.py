from fastapi import Depends

from app.feature.auth.adapter.output.persistence import AlchemyUserRepository
from app.feature.auth.application.port.input import SignUpCommand
from app.feature.auth.domain import User
from core.auth.utils import Encryptor


class SignUpUseCase:
    def __init__(
        self,
        user_repo: AlchemyUserRepository = Depends(),
        encryptor: Encryptor = Depends(),
    ):
        self.user_repo = user_repo
        self.encryptor = encryptor

    async def __call__(self, cmd: SignUpCommand) -> User:
        password = self.encryptor.hash(cmd.password)

        user = User.create(
            **cmd.model_dump(exclude={"password"}),
            password=password,
        )
        return await self.user_repo.create(user)
