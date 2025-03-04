from fastapi import Depends

from app.feature.auth.application.exception import AuthorizationException
from app.feature.auth.domain import User, UserLevel
from core.auth.dependency import get_current_user


class UserResourceAccessUseCase:
    def __init__(self, user: User = Depends(get_current_user)):
        self.user = user

    def __call__(self, user_id: str) -> None:
        if self.user.level == UserLevel.ADMIN:
            return

        if self.user.id != user_id:
            raise AuthorizationException()
