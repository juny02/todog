from fastapi import Cookie
from jose import JWTError
from jose.exceptions import ExpiredSignatureError
from core.auth.exceptions import ExpiredTokenException, InvalidTokenException, MissingTokenException
from api.core.auth.utils.AuthToken import Token


class VerifyToken:
    def __call__(self, access_token: str | None = Cookie(default=None)):
        
        if access_token is None:
            raise MissingTokenException
        
        if access_token.split(" ")[0] != "Bearer":
            raise InvalidTokenException
        
        access_token = access_token.split(" ")[1]
        token = Token(access_token)

        try:
            payload = token.decode()
        except ExpiredSignatureError:
            raise ExpiredTokenException
        except JWTError:
            raise InvalidTokenException

        expiration_date_unix = payload.get("exp")

        if expiration_date_unix is None:
            raise InvalidTokenException
