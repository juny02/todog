from typing import List

from fastapi import APIRouter, Depends, status

from app.walk_record.adapter.input.api.request.CreateWalkRecordRequest import (
    CreateWalkRecordRequest,
)
from app.walk_record.adapter.input.api.request.GetTreatRecordsRequest import (
    GetWalkRecordsRequest,
)
from app.walk_record.adapter.input.api.request.UpdateWalkRecordRequest import (
    UpdateWalkRecordRequest,
)
from app.walk_record.adapter.input.api.response.GetWalkRecordResponse import (
    GetWalkRecordResponse,
)
from app.walk_record.application.port.input.CreateWalkRecordCommand import (
    CreateWalkRecordCommand,
)
from app.walk_record.application.port.input.GetWalkRecordsCommand import (
    GetWalkRecordsCommand,
)
from app.walk_record.application.port.input.UpdateWalkRecordCommand import (
    UpdateWalkRecordCommand,
)
from app.walk_record.application.usecase.CreateWalkRecordUseCase import (
    CreateWalkRecordUseCase,
)
from app.walk_record.application.usecase.DeleteWalkRecordUseCase import (
    DeleteWalkRecordUseCase,
)
from app.walk_record.application.usecase.GetWalkRecordsUseCase import (
    GetWalkRecordsUseCase,
)
from app.walk_record.application.usecase.GetWalkRecordUseCase import (
    GetWalkRecordUseCase,
)
from app.walk_record.application.usecase.UpdateWalkRecordUseCase import (
    UpdateWalkRecordUseCase,
)

router = APIRouter(prefix="/dogs", tags=["WalkRecord"])


@router.post("/{dog_id}/walk_records", status_code=status.HTTP_201_CREATED)
async def post_walk_record(
    *,
    dog_id: str,
    body: CreateWalkRecordRequest,
    create_walk_record: CreateWalkRecordUseCase = Depends()
):
    cmd = CreateWalkRecordCommand(dog_id=dog_id, **body.model_dump())
    return await create_walk_record(cmd)


@router.get("/{dog_id}/walk_records", response_model=List[GetWalkRecordResponse])
async def get_walk_records_by_dog(
    *,
    dog_id: str,
    query: GetWalkRecordsRequest = Depends(),
    get_walk_records: GetWalkRecordsUseCase = Depends()
):
    cmd = GetWalkRecordsCommand(dog_id=dog_id, **query.model_dump())
    return await get_walk_records(cmd)


@router.get(
    "/{dog_id}/walk_records/{walk_record_id}", response_model=GetWalkRecordResponse
)
async def get_walk_record(
    *, dog_id: str, walk_record_id: str, get_by_id: GetWalkRecordUseCase = Depends()
):
    return await get_by_id(id=walk_record_id, dog_id=dog_id)


@router.patch(
    "/{dog_id}/walk_records/{walk_record_id}", response_model=GetWalkRecordResponse
)
async def patch_walk_record(
    *,
    dog_id: str,
    walk_record_id: str,
    body: UpdateWalkRecordRequest,
    update: UpdateWalkRecordUseCase = Depends()
):
    cmd = UpdateWalkRecordCommand(id=walk_record_id, dog_id=dog_id, **body.model_dump())
    return await update(cmd)


@router.delete(
    "/{dog_id}/walk_records/{walk_record_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_walk_record(
    *, dog_id: str, walk_record_id: str, delete: DeleteWalkRecordUseCase = Depends()
):
    await delete(id=walk_record_id, dog_id=dog_id)
