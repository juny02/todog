from typing import List

from fastapi import APIRouter, Depends, status

from app.memo.adapter.input.api.request.CreateMemoRequest import (
    CreateMemoRequest,
)
from app.memo.adapter.input.api.request.GetMemosRequest import GetMemosRequest
from app.memo.adapter.input.api.request.UpdateMemoRequest import (
    UpdateMemoRequest,
)
from app.memo.adapter.input.api.response.GetMemoResponse import (
    GetMemoResponse,
)
from app.memo.application.port.input.CreateMemoCommand import (
    CreateMemoCommand,
)
from app.memo.application.port.input.GetMemosCommand import GetMemosCommand
from app.memo.application.port.input.UpdateMemoCommand import (
    UpdateMemoCommand,
)
from app.memo.application.usecase.CreateMemoUseCase import CreateMemoUseCase
from app.memo.application.usecase.DeleteMemoUseCase import DeleteMemoUseCase
from app.memo.application.usecase.GetMemosUseCase import (
    GetMemosUseCase,
)
from app.memo.application.usecase.GetMemoUseCase import GetMemoUseCase
from app.memo.application.usecase.UpdateMemoUseCase import UpdateMemoUseCase

router = APIRouter(prefix="/dogs", tags=["Memo"])


@router.post(
    "/{dog_id}/memos",
    response_model=GetMemoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_memo(
    *, dog_id: str, body: CreateMemoRequest, create_memo: CreateMemoUseCase = Depends()
):
    cmd = CreateMemoCommand(dog_id=dog_id, **body.model_dump())
    return await create_memo(cmd)


@router.get("/{dog_id}/memos", response_model=List[GetMemoResponse])
async def get_memos_by_dog(
    *,
    dog_id: str,
    query: GetMemosRequest = Depends(),
    get_memos: GetMemosUseCase = Depends()
):
    cmd = GetMemosCommand(dog_id=dog_id, **query.model_dump())
    return await get_memos(cmd)


@router.get("/{dog_id}/memos/{memo_id}", response_model=GetMemoResponse)
async def get_memo(*, dog_id: str, memo_id: str, get_by_id: GetMemoUseCase = Depends()):
    return await get_by_id(id=memo_id, dog_id=dog_id)


@router.patch("/{dog_id}/memos/{memo_id}", response_model=GetMemoResponse)
async def patch_memo(
    *,
    dog_id: str,
    memo_id: str,
    body: UpdateMemoRequest,
    update: UpdateMemoUseCase = Depends()
):
    cmd = UpdateMemoCommand(id=memo_id, dog_id=dog_id, **body.model_dump())
    return await update(cmd)


@router.delete("/{dog_id}/memos/{memo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memo(
    *, dog_id: str, memo_id: str, delete: DeleteMemoUseCase = Depends()
):
    await delete(id=memo_id, dog_id=dog_id)
