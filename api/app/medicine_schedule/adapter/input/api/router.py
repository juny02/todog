from typing import List

from fastapi import APIRouter, Depends, status

from app.medicine_schedule.adapter.input.api.request.CreateMedScheduleRequest import (
    CreateMedScheduleRequest,
)
from app.medicine_schedule.adapter.input.api.request.GetMedSchedulesRequest import (
    GetMedSchedulesRequest,
)
from app.medicine_schedule.adapter.input.api.request.UpdateMedScheduleRequest import (
    UpdateMedScheduleRequest,
)
from app.medicine_schedule.adapter.input.api.response.GetMedScheduleResponse import (
    GetMedScheduleResponse,
)
from app.medicine_schedule.application.port.input.CreateMedScheduleCommand import (
    CreateMedScheduleCommand,
)
from app.medicine_schedule.application.port.input.GetMedSchedulesCommand import (
    GetMedSchedulesCommand,
)
from app.medicine_schedule.application.port.input.UpdateMedScheduleCommand import (
    UpdateMedScheduleCommand,
)
from app.medicine_schedule.application.usecase.CreateMedScheduleUseCase import (
    CreateMedScheduleUseCase,
)
from app.medicine_schedule.application.usecase.DeleteMedScheduleUseCase import (
    DeleteMedScheduleUseCase,
)
from app.medicine_schedule.application.usecase.GetMedSchedulesUseCase import (
    GetMedSchedulesUseCase,
)
from app.medicine_schedule.application.usecase.GetMedScheduleUseCase import GetMedScheduleUseCase
from app.medicine_schedule.application.usecase.UpdateMedScheduleUseCase import (
    UpdateMedScheduleUseCase,
)

router = APIRouter(prefix="/dogs", tags=["MedSchedule"])


@router.post(
    "/{dog_id}/medicine_schedules",
    response_model=GetMedScheduleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_medicine_schedule(
    *, dog_id: str, body: CreateMedScheduleRequest, create_medicine_schedule: CreateMedScheduleUseCase = Depends()
):
    cmd = CreateMedScheduleCommand(dog_id=dog_id, **body.model_dump())
    return await create_medicine_schedule(cmd)


@router.get("/{dog_id}/medicine_schedules", response_model=List[GetMedScheduleResponse])
async def get_medicine_schedules_by_dog(
    *,
    dog_id: str,
    query: GetMedSchedulesRequest = Depends(),
    get_medicine_schedules: GetMedSchedulesUseCase = Depends()
):
    cmd = GetMedSchedulesCommand(dog_id=dog_id, **query.model_dump())
    return await get_medicine_schedules(cmd)


@router.get("/{dog_id}/medicine_schedules/{medicine_schedule_id}", response_model=GetMedScheduleResponse)
async def get_medicine_schedule(*, dog_id: str, medicine_schedule_id: str, get_by_id: GetMedScheduleUseCase = Depends()):
    return await get_by_id(id=medicine_schedule_id, dog_id=dog_id)


@router.patch("/{dog_id}/medicine_schedules/{medicine_schedule_id}", response_model=GetMedScheduleResponse)
async def patch_medicine_schedule(
    *,
    dog_id: str,
    medicine_schedule_id: str,
    body: UpdateMedScheduleRequest,
    update: UpdateMedScheduleUseCase = Depends()
):
    cmd = UpdateMedScheduleCommand(id=medicine_schedule_id, dog_id=dog_id, **body.model_dump())
    return await update(cmd)


@router.delete("/{dog_id}/medicine_schedules/{medicine_schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicine_schedule(
    *, dog_id: str, medicine_schedule_id: str, delete: DeleteMedScheduleUseCase = Depends()
):
    await delete(id=medicine_schedule_id, dog_id=dog_id)
