from fastapi import HTTPException, status

ExpiredTokenException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The token has expired",
    headers={"WWW-Authenticate": "Bearer error='invalid_token' error_error_description='The token has expired'"},
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The token is not valid.",
    headers={"WWW-Authenticate": "Bearer error='invalid_token' error_error_description='The token is not valid.'"},
)

MissingTokenException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Token is missing.",
    headers={"WWW-Authenticate": "Bearer error='missing_token' error_error_description='Token is missing.'"},
)

InvalidPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The password is not valid.",
    headers={"WWW-Authenticate": "Bearer error='invalid_password' error_error_description='The password is not valid.'"},
)