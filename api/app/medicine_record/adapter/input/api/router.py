from typing import List

from fastapi import APIRouter, Depends, status

from app.medicine_record.adapter.input.api.request.CreateMedRecordRequest import (
    CreateMedRecordRequest,
)
from app.medicine_record.adapter.input.api.request.GetMedRecordsRequest import GetMedRecordsRequest
from app.medicine_record.adapter.input.api.request.UpdateMedRecordRequest import (
    UpdateMedRecordRequest,
)
from app.medicine_record.adapter.input.api.response.GetMedRecordResponse import (
    GetMedRecordResponse,
)
from app.medicine_record.application.port.input.CreateMedRecordCommand import (
    CreateMedRecordCommand,
)
from app.medicine_record.application.port.input.GetMedRecordsCommand import GetMedRecordsCommand
from app.medicine_record.application.port.input.UpdateMedRecordCommand import (
    UpdateMedRecordCommand,
)
from app.medicine_record.application.usecase.CreateMedRecordUseCase import (
    CreateMedRecordUseCase,
)
from app.medicine_record.application.usecase.DeleteMedRecordUseCase import (
    DeleteMedRecordUseCase,
)
from app.medicine_record.application.usecase.GetMedRecordsUseCase import (
    GetMedRecordsUseCase,
)
from app.medicine_record.application.usecase.GetMedRecordUseCase import (
    GetMedRecordUseCase,
)
from app.medicine_record.application.usecase.UpdateMedRecordUseCase import (
    UpdateMedRecordUseCase,
)

router = APIRouter(prefix="/dogs", tags=["MedRecord"])


@router.post("/{dog_id}/medicine_records", status_code=status.HTTP_201_CREATED)
async def post_medicine_record(
    *,
    dog_id: str,
    body: CreateMedRecordRequest,
    create_medicine_record: CreateMedRecordUseCase = Depends()
):
    cmd = CreateMedRecordCommand(dog_id=dog_id, **body.model_dump())
    return await create_medicine_record(cmd)


@router.get("/{dog_id}/medicine_records", response_model=List[GetMedRecordResponse])
async def get_medicine_records_by_dog(
    *,
    dog_id: str,
    query: GetMedRecordsRequest = Depends(),
    get_medicine_records: GetMedRecordsUseCase = Depends()
):
    cmd = GetMedRecordsCommand(dog_id=dog_id, **query.model_dump())
    return await get_medicine_records(cmd)


@router.get(
    "/{dog_id}/medicine_records/{medicine_record_id}", response_model=GetMedRecordResponse
)
async def get_medicine_record(
    *, dog_id: str, medicine_record_id: str, get_by_id: GetMedRecordUseCase = Depends()
):
    return await get_by_id(id=medicine_record_id, dog_id=dog_id)


@router.patch(
    "/{dog_id}/medicine_records/{medicine_record_id}", response_model=GetMedRecordResponse
)
async def patch_medicine_record(
    *,
    dog_id: str,
    medicine_record_id: str,
    body: UpdateMedRecordRequest,
    update: UpdateMedRecordUseCase = Depends()
):
    cmd = UpdateMedRecordCommand(id=medicine_record_id, dog_id=dog_id, **body.model_dump())
    return await update(cmd)


@router.delete(
    "/{dog_id}/medicine_records/{medicine_record_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_medicine_record(
    *, dog_id: str, medicine_record_id: str, delete: DeleteMedRecordUseCase = Depends()
):
    await delete(id=medicine_record_id, dog_id=dog_id)
