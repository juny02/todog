import os

from fastapi import Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api.core.auth.utils.AuthToken import Token
from core.auth.exceptions import InvalidPasswordException

SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD", None)

class PasswordRequest(BaseModel):
    password: str
    
class VerifySuperUser:
    def __init__(self, body: PasswordRequest = Body(...)):
        self.password = body.password 

    async def __call__(self) -> JSONResponse:
        if self.password != SUPERUSER_PASSWORD:
            raise InvalidPasswordException
        
        # issue new token
        token = Token()
        return token.set_cookie()