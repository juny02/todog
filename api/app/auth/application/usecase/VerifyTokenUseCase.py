
from api.core.auth.utils import AuthToken
from app.feature.auth.adapter.output.persistence.RedisTokenRepository import (
    RedisTokenRepository,
)
from app.feature.auth.domain import User
from core.auth.utils import OAuth2PasswordBearerWithCookie
from core.auth.utils.JsonEncoder import get_decode_token

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")
from fastapi import Depends
from jose.exceptions import ExpiredSignatureError

from app.feature.auth.adapter.output.persistence import AlchemyUserRepository
from app.feature.auth.application.exception import (
    ExpiredCredentialsException,
    InvalidAuthenticationTokenException,
)


class VerifyTokenUseCase:
    def __init__(
        self,
        user_repo: AlchemyUserRepository = Depends(),
        token_repo: RedisTokenRepository = Depends(),
        token: AuthToken = Depends(oauth2_scheme),
    ):
        self.token = token
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def __call__(self) -> User:
        try:
            payload = get_decode_token(self.token.access_token)
        except ExpiredSignatureError:
            raise ExpiredCredentialsException

        username = payload.get("sub")
        expiration_date_unix = payload.get("exp")

        if username is None:
            raise InvalidAuthenticationTokenException

        if expiration_date_unix is None:
            raise InvalidAuthenticationTokenException

        user = await self.user_repo.get_by_username(username=username)

        stored_access_token = self.token_repo.get_access_token(user.id)

        if stored_access_token != self.token.access_token:
            raise InvalidAuthenticationTokenException

        user = await self.user_repo.get_by_username(username)
        return user
