from abc import ABC, abstractmethod
from api.core.auth.utils import AuthToken
class TokenRepository(ABC):
    @abstractmethod
    async def store(self, user_id: str, token: AuthToken) -> str:
        pass
    @abstractmethod
    def get_access_token(self, user_id: str) -> str:
        pass
    @abstractmethod
    def get_refresh_token(self, user_id: str) -> str:
        pass
    @abstractmethod
    def delete(self, user_id: str) -> str:
        pass