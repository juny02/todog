from typing import List

from fastapi import APIRouter, Depends, status

from app.meal_record.adapter.input.api.request.CreateMealRecordRequest import (
    CreateMealRecordRequest,
)
from app.meal_record.adapter.input.api.request.UpdateMealRecordRequest import (
    UpdateMealRecordRequest,
)
from app.meal_record.adapter.input.api.response.GetMealRecordResponse import (
    GetMealRecordResponse,
)
from app.meal_record.application.port.input.CreateMealRecordCommand import (
    CreateMealRecordCommand,
)
from app.meal_record.application.port.input.UpdateMealRecordCommand import (
    UpdateMealRecordCommand,
)
from app.meal_record.application.usecase.CreateMealRecordUseCase import CreateMealRecordUseCase
from app.meal_record.application.usecase.DeleteMealRecordUseCase import DeleteMealRecordUseCase
from app.meal_record.application.usecase.GetMealRecordsByDogUseCase import (
    GetMealRecordsByDogUseCase,
)
from app.meal_record.application.usecase.GetMealRecordUseCase import GetMealRecordUseCase
from app.meal_record.application.usecase.UpdateMealRecordUseCase import UpdateMealRecordUseCase

router = APIRouter(prefix="/dogs", tags=["MealRecord"])


@router.post("/{dog_id}/meal_records", status_code=status.HTTP_201_CREATED)
async def post_meal_record(
    *,
    dog_id: str,
    body: CreateMealRecordRequest,
    create_meal_record: CreateMealRecordUseCase = Depends()
):
    cmd = CreateMealRecordCommand(dog_id=dog_id, **body.model_dump())
    return await create_meal_record(cmd)
    
@router.get("/{dog_id}/meal_records", response_model=List[GetMealRecordResponse])
async def get_meal_records_by_dog(
    *, dog_id: str, get_meal_records: GetMealRecordsByDogUseCase = Depends()
):
    return await get_meal_records(dog_id)

@router.get("/{dog_id}/meal_records/{meal_record_id}", response_model=GetMealRecordResponse)
async def get_meal_record(
    *, dog_id: str, meal_record_id: str, get_by_id: GetMealRecordUseCase = Depends()
):
    return await get_by_id(id=meal_record_id, dog_id=dog_id)

@router.patch("/{dog_id}/meal_records/{meal_record_id}", response_model=GetMealRecordResponse)
async def patch_meal_record(
    *,
    dog_id: str,
    meal_record_id: str,
    body: UpdateMealRecordRequest,
    update: UpdateMealRecordUseCase = Depends()
):
    cmd = UpdateMealRecordCommand(id=meal_record_id, dog_id=dog_id, **body.model_dump())
    return await update(cmd)

@router.delete("/{dog_id}/meal_records/{meal_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meal_record(
    *, dog_id: str, meal_record_id: str, delete: DeleteMealRecordUseCase = Depends()
):
    await delete(id=meal_record_id, dog_id=dog_id)