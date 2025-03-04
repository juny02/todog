import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends

from api.app.user.adapter.output.persistence.repository.UserSQLModelRepository import UserSQLModelRepository
from api.core.auth.utils import AuthToken
from app.feature.auth.adapter.output.persistence.RedisTokenRepository import RedisTokenRepository
from app.feature.auth.application.exception import WrongPasswordError
from app.feature.auth.application.port.input import SignInCommand
from app.feature.auth.domain import User
from core.auth.utils import Encryptor
from core.auth.utils.JsonEncoder import get_encode_token

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("AUTH_TOKEN_LIFE_MINUTE", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("AUTH_TOKEN_LIFE_DAY", 30))
fake_refresh_token_storage = dict()  # TODO : timeout 지원해야함


class SignInUseCase:
    def __init__(
        self,
        user_repo: UserSQLModelRepository = Depends(),
        token_repo: RedisTokenRepository = Depends(),

        encryptor: Encryptor = Depends(),
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.encryptor = encryptor

    async def __call__(self, cmd: SignInCommand):
        user = await self.user_repo.get_by_username(username=cmd.username)

        await self.authenticate(username=cmd.username, input_password=cmd.password)

        token = self.create_token(user)

        self.store_token(user, token)

        return user, token

    def create_token(self, user: User) -> AuthToken:

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        access_token = self.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        refresh_token = self.create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)

        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    async def authenticate(self, username: str, input_password: str):
        user = await self.user_repo.get_by_username(username)

        if not self.encryptor.verify(input_password, user.password):
            raise WrongPasswordError

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_data = get_encode_token(to_encode)
        return encoded_data

    def create_refresh_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_data = get_encode_token(to_encode)
        fake_refresh_token_storage[data["sub"]] = encoded_data
        return encoded_data

    def store_token(self, user: User, token: AuthToken):
        return self.token_repo.store(user_id=user.id, token=token)