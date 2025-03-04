import os

import redis
from fastapi.params import Depends

from app.feature.auth.adapter.output.persistence.TokenMapper import TokenMapper
from app.feature.auth.adapter.output.persistence.TokenRepository import TokenRepository
from app.feature.auth.application.exception import ExpiredCredentialsException
from api.core.auth.utils import AuthToken
from core.db.dependency import get_redis

ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("AUTH_TOKEN_LIFE_MINUTE", 30)) * 60
REFRESH_TOKEN_EXPIRE_SECONDS = int(os.getenv("AUTH_TOKEN_LIFE_DAY", 30)) * 24 * 60 * 60

class RedisTokenRepository(TokenRepository):
    def __init__(self, redis_client: redis.Redis = Depends(get_redis)):
        self.redis_client = redis_client

    def store(self, user_id: str, token: AuthToken) -> str:
        access_token_key = TokenMapper.user_id_to_access_token_key(user_id)
        refresh_token_key = TokenMapper.user_id_to_refresh_token_key(user_id)
        self.redis_client.setex(name=access_token_key, time=ACCESS_TOKEN_EXPIRE_SECONDS, value=token.access_token)
        self.redis_client.setex(name=refresh_token_key, time=REFRESH_TOKEN_EXPIRE_SECONDS, value=token.refresh_token)
        return user_id

    def get_access_token(self, user_id: str) -> str:
        try:
            key = TokenMapper.user_id_to_access_token_key(user_id)
            access_token = self.redis_client.get(name=key).decode("utf-8")
        except:
            raise ExpiredCredentialsException
        return access_token

    def get_refresh_token(self, user_id: str) -> str:
        try:
            key = TokenMapper.user_id_to_refresh_token_key(user_id)
            refresh_token = self.redis_client.get(name=key).decode("utf-8")
        except:
            raise ExpiredCredentialsException
        return refresh_token

    def delete(self, user_id: str) -> str:
        access_token_key = TokenMapper.user_id_to_access_token_key(user_id)
        refresh_token_key = TokenMapper.user_id_to_refresh_token_key(user_id)
        self.redis_client.delete(access_token_key, refresh_token_key)
        return user_id