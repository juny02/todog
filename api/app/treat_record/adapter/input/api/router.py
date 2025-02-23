from typing import List

from fastapi import APIRouter, Depends, status

from app.treat_record.adapter.input.api.request.CreateTreatRecordRequest import (
    CreateTreatRecordRequest,
)
from app.treat_record.adapter.input.api.request.UpdateTreatRecordRequest import (
    UpdateTreatRecordRequest,
)
from app.treat_record.adapter.input.api.response.GetTreatRecordResponse import (
    GetTreatRecordResponse,
)
from app.treat_record.application.port.input.CreateTreatRecordCommand import (
    CreateTreatRecordCommand,
)
from app.treat_record.application.port.input.UpdateTreatRecordCommand import (
    UpdateTreatRecordCommand,
)
from app.treat_record.application.usecase.CreateTreatRecordUseCase import CreateTreatRecordUseCase
from app.treat_record.application.usecase.DeleteTreatRecordUseCase import DeleteTreatRecordUseCase
from app.treat_record.application.usecase.GetTreatRecordsByDogUseCase import (
    GetTreatRecordsByDogUseCase,
)
from app.treat_record.application.usecase.GetTreatRecordUseCase import GetTreatRecordUseCase
from app.treat_record.application.usecase.UpdateTreatRecordUseCase import UpdateTreatRecordUseCase

router = APIRouter(prefix="/dogs", tags=["TreatRecord"])


@router.post("/{dog_id}/treat_records", status_code=status.HTTP_201_CREATED)
async def post_treat_record(
    *,
    dog_id: str,
    body: CreateTreatRecordRequest,
    create_treat_record: CreateTreatRecordUseCase = Depends()
):
    cmd = CreateTreatRecordCommand(dog_id=dog_id, **body.model_dump())
    return await create_treat_record(cmd)
    
@router.get("/{dog_id}/treat_records", response_model=List[GetTreatRecordResponse])
async def get_treat_records_by_dog(
    *, dog_id: str, get_treat_records: GetTreatRecordsByDogUseCase = Depends()
):
    return await get_treat_records(dog_id)

@router.get("/{dog_id}/treat_records/{treat_record_id}", response_model=GetTreatRecordResponse)
async def get_treat_record(
    *, dog_id: str, treat_record_id: str, get_by_id: GetTreatRecordUseCase = Depends()
):
    return await get_by_id(id=treat_record_id, dog_id=dog_id)

@router.patch("/{dog_id}/treat_records/{treat_record_id}", response_model=GetTreatRecordResponse)
async def patch_treat_record(
    *,
    dog_id: str,
    treat_record_id: str,
    body: UpdateTreatRecordRequest,
    update: UpdateTreatRecordUseCase = Depends()
):
    cmd = UpdateTreatRecordCommand(id=treat_record_id, dog_id=dog_id, **body.model_dump())
    return await update(cmd)

@router.delete("/{dog_id}/treat_records/{treat_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_treat_record(
    *, dog_id: str, treat_record_id: str, delete: DeleteTreatRecordUseCase = Depends()
):
    await delete(id=treat_record_id, dog_id=dog_id)