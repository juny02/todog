from fastapi import Depends
from jose import ExpiredSignatureError

from api.core.auth.utils import AuthToken
from app.feature.auth.adapter.output.persistence import AlchemyUserRepository
from app.feature.auth.adapter.output.persistence.RedisTokenRepository import RedisTokenRepository
from app.feature.auth.application.exception import ExpiredCredentialsException, InvalidAuthenticationTokenException
from core.auth.utils import OAuth2PasswordBearerWithCookie
from core.auth.utils.JsonEncoder import get_decode_token

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

class SignOutUseCase:
    def __init__(
        self,
        user_repo: AlchemyUserRepository = Depends(),
        token_repo: RedisTokenRepository = Depends(),
        token: AuthToken = Depends(oauth2_scheme)
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.token = token

    async def __call__(self):
        try:
            payload = get_decode_token(self.token.access_token)
        except ExpiredSignatureError:
            raise ExpiredCredentialsException

        username = payload.get("sub")
        if username is None:
            raise InvalidAuthenticationTokenException

        user = await self.user_repo.get_by_username(username=username)

        access_token = self.token_repo.get_access_token(user.id)

        if access_token == "None":
            raise InvalidAuthenticationTokenException

        self.token_repo.delete(user_id=user.id)

        return user, self.token