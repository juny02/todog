from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.app.auth.adapter.input.api.request.SignInRequest import SignInRequest
from api.app.auth.application.port.input.SignInCommand import SignInCommand
from api.app.auth.application.usecase.SignInUseCase import SignInUseCase

auth_router = APIRouter(tags=["User"])


# @auth_router.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     response: Response,
# ):
#     try:
#         token = await sign_in(form_data.username, form_data.password)
#         token.paste_to_cookie(response)
#         return {"token_type": token.token_type, "expires_in": token.expires_in}
#     except UserEntityNotFoundError:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user " + form_data.username + "does not exist")


@auth_router.post("/signin")
async def sign_in(
    *,
    request: SignInRequest,
    response: Response,
    sign_in: SignInUseCase = Depends(),
):
    try:
        cmd = SignInCommand(**request.model_dump())
        user, token = await sign_in(cmd)

        token.paste_to_cookie(response)
        return user
    except UserNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.message))
    except WrongPasswordError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.message))


@auth_router.post("/signup")
async def sign_up(
    *,
    body_params: SignUpBodyParams,
    sign_up: SignUpUseCase = Depends(),
):
    try:
        cmd = SignUpCommand(**body_params.model_dump())

        user = await sign_up(cmd)
        return user
    except UserDuplicatedException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/signout")
async def sign_out(
    *,
    sign_out: SignOutUseCase = Depends(),
    response: Response
):
    try:
        user, token = await sign_out()
        token.delete_to_cookie(response)
        return user
    except (InvalidAuthenticationTokenException, ExpiredCredentialsException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e.message))


@auth_router.get("/auth/verify")
async def verify_token(
    *,
    verify_token: VerifyTokenUseCase = Depends(),
):
    try:
        user = await verify_token()
        return user
    except ExpiredCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.get("/auth/reissue")
async def reissue_token(
    *,
    reissue_token: ReissueTokenUseCase = Depends(),
    response: Response
):
    try:
        token = await reissue_token()
        token.paste_to_cookie(response)
        return HTTPStatus.OK
    except (InvalidAuthenticationTokenException, ExpiredCredentialsException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except InvalidTokenReissueRequestException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@auth_router.get("/get_me")
async def get_me(
    *,
    verify_token: VerifyTokenUseCase = Depends(),
):
    """
    Access token을 기반으로 현재 유저 정보를 불러옵니다.

    Returns:
        User: 현재 유저 정보

    Throws:
        HTTPException: 유효하지 않은 access token 또는 만료된 access token
    """
    try:
        user = await verify_token()
        return user
    except (InvalidAuthenticationTokenException, ExpiredCredentialsException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)


# @auth_router.post("/auth/refresh")
# async def refresh_all_token(
#     response: Response,
#     grant_type: Annotated[str, Query()],
#     token: Token = Depends(oauth2_scheme),
# ):
#     if grant_type == "refresh_token":
#         new_token = await refresh_token(token)
#         new_token.paste_to_cookie(response)

#         return {}
#     else:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported grant type")
