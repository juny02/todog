from fastapi import Depends

from app.feature.auth.adapter.output.persistence import AlchemyUserRepository
from app.feature.auth.application.port.input import UpdateUserCommand
from app.feature.auth.domain import User
from core.auth.utils.Encryptor import Encryptor


class UpdateUserUseCase:
    def __init__(
        self,
        user_repo: AlchemyUserRepository = Depends(),
        encryptor: Encryptor = Depends(),
    ):
        self.user_repo = user_repo
        self.encryptor = encryptor

    async def __call__(self, cmd: UpdateUserCommand) -> User:
        user = await self.user_repo.get_by_id(cmd.user_id)

        update_data = cmd.model_dump(
            exclude={"user_id"}, exclude_unset=True, exclude_defaults=True)

        # 비밀번호는 encryption 필요
        if "password" in update_data:
            update_data["password"] = self.encryptor.hash(
                update_data["password"])

        for key, value in update_data.items():
            setattr(user, key, value)

        return await self.user_repo.update(user)
