from datetime import datetime, timedelta, timezone
import os
from fastapi.responses import JSONResponse
from jose import jwt
from core.auth.exceptions  import (
    ExpiredTokenException,
    InvalidTokenException,
)

SECRET_KEY = os.getenv("SECRET_KEY", None)
ALGORITHM = os.getenv("AUTH_ALGORITHM", "HS256")


class AuthToken:
    def __init__(self, user_id: str = "user_auth", expire_dates: int = 15, token: str = None,):
        if token is None:
            self.token = self._issue(user_id, expire_dates)  
        else:
            self.token = token

    def set_cookie(self, http_only: bool = True) -> JSONResponse:
        response = JSONResponse(content={"message": "Success"})  
        response.set_cookie(key="access_token", value=f"Bearer {self.token}", httponly=http_only)
        return response
    

    def decode(self):
        return jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
    
    def _issue(self, user_id: str, expire_dates: int):
        expire = datetime.now(timezone.utc) + timedelta(days=expire_dates)
        
        base_payload = {
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "sub": user_id,
        }
        
        return jwt.encode(base_payload, SECRET_KEY, algorithm=ALGORITHM)
