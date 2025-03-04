import os
from datetime import datetime, timedelta, timezone

from fastapi.params import Depends
from jose import ExpiredSignatureError, JWTError

from api.core.auth.utils import AuthToken
from app.feature.auth.adapter.output.persistence import AlchemyUserRepository
from app.feature.auth.adapter.output.persistence.RedisTokenRepository import RedisTokenRepository
from app.feature.auth.application.exception import (
    ExpiredCredentialsException,
    InvalidAuthenticationTokenException,
    InvalidTokenReissueRequestException,
)
from core.auth.utils import OAuth2PasswordBearerWithCookie
from core.auth.utils.JsonEncoder import get_decode_token, get_encode_token

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("AUTH_TOKEN_LIFE_MINUTE", 30))


class ReissueTokenUseCase:
    def __init__(
        self,
        user_repo: AlchemyUserRepository = Depends(),
        token_repo: RedisTokenRepository = Depends(),
        token: AuthToken = Depends(oauth2_scheme)
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.token = token

    async def __call__(self) -> AuthToken:
        try:
            payload = get_decode_token(self.token.access_token)
            username = payload.get("sub")
            if username is None:
                raise InvalidAuthenticationTokenException

            return await self.reissue_token()

        except (ExpiredSignatureError, JWTError):
            return await self.reissue_token()
        except Exception as e:
            raise e

    async def reissue_token(self) -> AuthToken:
        try:
            payload = get_decode_token(self.token.refresh_token)
        except ExpiredSignatureError:
            raise ExpiredCredentialsException()
        except JWTError:
            raise InvalidAuthenticationTokenException()

        username = payload.get("sub")
        if username is None:
            raise InvalidAuthenticationTokenException

        user = await self.user_repo.get_by_username(username)
        if user is None:
            raise InvalidAuthenticationTokenException

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires)

        new_token = AuthToken(
            access_token=new_access_token,
            refresh_token=self.token.refresh_token,
            token_type=self.token.token_type,
        )

        # 새로운 토큰 Redis에 저장하도록 함.
        self.token_repo.store(user_id=user.id, token=new_token)

        return new_token

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta

        to_encode.update({"exp": expire})
        encoded_token = get_encode_token(to_encode)
        return encoded_token
