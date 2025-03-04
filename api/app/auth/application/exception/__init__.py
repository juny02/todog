from fastapi import status

from app.feature.exception import (
    BaseException,
    DuplicatedException,
    NotFoundException,
    ValidationException,
)


class AuthenticationException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "인증이 실패했습니다. 유효한 자격 증명을 제공하십시오."
    headers = {"WWW-Authenticate": "Bearer"}


class AuthorizationException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "접근 권한이 제한되었습니다. 권한을 확인한 후 다시 시도해 주세요."


class ExpiredCredentialsException(AuthenticationException):
    message = "자격 증명이 만료되었습니다. 다시 로그인 해주세요."


class InvalidAuthenticationTokenException(AuthenticationException):
    message = "유효하지 않은 인증 토큰입니다. 새로운 토큰을 발급받아 시도해 주세요."

class InvalidTokenReissueRequestException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "유효하지 않은 재발급 요청입니다. 인증 토큰의 만료기간을 다시 확인해 주세요."


class UserNotFoundException(NotFoundException):
    pass


class UserDuplicatedException(DuplicatedException):
    pass


class WrongPasswordError(ValidationException):
    pass
