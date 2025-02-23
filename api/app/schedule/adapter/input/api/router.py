from typing import List

from fastapi import APIRouter, Depends, status

from app.schedule.adapter.input.api.request.CreateScheduleRequest import (
    CreateScheduleRequest,
)
from app.schedule.adapter.input.api.request.GetSchedulesRequest import GetSchedulesRequest
from app.schedule.adapter.input.api.request.UpdateScheduleRequest import (
    UpdateScheduleRequest,
)
from app.schedule.adapter.input.api.response.GetScheduleResponse import (
    GetScheduleResponse,
)
from app.schedule.application.port.input.CreateScheduleCommand import (
    CreateScheduleCommand,
)
from app.schedule.application.port.input.GetSchedulesCommand import GetSchedulesCommand
from app.schedule.application.port.input.UpdateScheduleCommand import (
    UpdateScheduleCommand,
)
from app.schedule.application.usecase.CreateScheduleUseCase import CreateScheduleUseCase
from app.schedule.application.usecase.DeleteScheduleUseCase import DeleteScheduleUseCase
from app.schedule.application.usecase.GetSchedulesUseCase import (
    GetSchedulesUseCase,
)
from app.schedule.application.usecase.GetScheduleUseCase import GetScheduleUseCase
from app.schedule.application.usecase.UpdateScheduleUseCase import UpdateScheduleUseCase

router = APIRouter(prefix="/dogs", tags=["Schedule"])


@router.post(
    "/{dog_id}/schedules",
    response_model=GetScheduleResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_schedule(
    *, dog_id: str, body: CreateScheduleRequest, create_schedule: CreateScheduleUseCase = Depends()
):
    cmd = CreateScheduleCommand(dog_id=dog_id, **body.model_dump())
    return await create_schedule(cmd)


@router.get("/{dog_id}/schedules", response_model=List[GetScheduleResponse])
async def get_schedules_by_dog(
    *,
    dog_id: str,
    query: GetSchedulesRequest = Depends(),
    get_schedules: GetSchedulesUseCase = Depends()
):
    cmd = GetSchedulesCommand(dog_id=dog_id, **query.model_dump())
    return await get_schedules(cmd)


@router.get("/{dog_id}/schedules/{schedule_id}", response_model=GetScheduleResponse)
async def get_schedule(*, dog_id: str, schedule_id: str, get_by_id: GetScheduleUseCase = Depends()):
    return await get_by_id(id=schedule_id, dog_id=dog_id)


@router.patch("/{dog_id}/schedules/{schedule_id}", response_model=GetScheduleResponse)
async def patch_schedule(
    *,
    dog_id: str,
    schedule_id: str,
    body: UpdateScheduleRequest,
    update: UpdateScheduleUseCase = Depends()
):
    cmd = UpdateScheduleCommand(id=schedule_id, dog_id=dog_id, **body.model_dump())
    return await update(cmd)


@router.delete("/{dog_id}/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(
    *, dog_id: str, schedule_id: str, delete: DeleteScheduleUseCase = Depends()
):
    await delete(id=schedule_id, dog_id=dog_id)
