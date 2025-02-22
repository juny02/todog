from typing import List

from fastapi import APIRouter, Depends, status

from app.user.adapter.input.api.request.CreateUserRequest import CreateUserRequest
from app.user.adapter.input.api.request.GetUsersRequest import GetUsersRequest
from app.user.adapter.input.api.request.UpdateUserRequest import UpdateUserRequest
from app.user.adapter.input.api.response.GetUserResponse import GetUserResponse
from app.user.application.port.input.CreateUserCommand import CreateUserCommand
from app.user.application.port.input.GetUsersCommand import GetUsersCommand
from app.user.application.port.input.UpdateUserCommand import UpdateUserCommand
from app.user.application.usecase.CreateUserUseCase import CreateUserUseCase
from app.user.application.usecase.DeleteUserUseCase import DeleteUserUseCase
from app.user.application.usecase.GetUsersUseCase import GetUsersUseCase
from app.user.application.usecase.GetUserUseCase import GetUserUseCase
from app.user.application.usecase.UpdatUserUseCase import UpdateUserUseCase

router = APIRouter(prefix="/users", tags=["User"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_user(*, body: CreateUserRequest, create_User: CreateUserUseCase = Depends()):
    cmd = CreateUserCommand(**body.model_dump())

    return await create_User(cmd)


@router.get("", response_model=List[GetUserResponse])
async def get_Users(
    *, query: GetUsersRequest = Depends(), get_all: GetUsersUseCase = Depends()
):
    cmd = GetUsersCommand(**query.model_dump())

    return await get_all(cmd)


@router.get("/{id}", response_model=GetUserResponse)
async def get_User(*, id: str, get_by_id: GetUserUseCase = Depends()):
    return await get_by_id(id)


@router.patch("/{id}", response_model=GetUserResponse)
async def patch_User(
    *, id: str, body: UpdateUserRequest, update: UpdateUserUseCase = Depends()
):
    cmd = UpdateUserCommand(id=id, **body.model_dump())
    return await update(cmd)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_User(*, id: str, delete: DeleteUserUseCase = Depends()):
    await delete(id)