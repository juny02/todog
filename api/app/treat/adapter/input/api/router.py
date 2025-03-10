from typing import List

from fastapi import APIRouter, Depends, status

from app.treat.adapter.input.api.request.CreateTreatRequest import CreateTreatRequest
from app.treat.adapter.input.api.request.UpdateTreatRequest import UpdateTreatRequest
from app.treat.adapter.input.api.response.GetTreatResponse import GetTreatResponse
from app.treat.application.port.input.CreateTreatCommand import CreateTreatCommand
from app.treat.application.port.input.UpdateTreatCommand import UpdateTreatCommand
from app.treat.application.usecase.CreateTreatUseCase import CreateTreatUseCase
from app.treat.application.usecase.DeleteTreatUseCase import DeleteTreatUseCase
from app.treat.application.usecase.GetTreatsByDogUseCase import GetTreatsByDogUseCase
from app.treat.application.usecase.GetTreatUseCase import GetTreatUseCase
from app.treat.application.usecase.UpdateTreatUseCase import UpdateTreatUseCase

router = APIRouter(prefix="/dogs", tags=["Treats"])


@router.post("/{dog_id}/treats", status_code=status.HTTP_201_CREATED)
async def post_treat(
    *,
    dog_id: str,
    body: CreateTreatRequest,
    create_treat: CreateTreatUseCase = Depends()
):
    cmd = CreateTreatCommand(dog_id=dog_id, **body.model_dump())
    return await create_treat(cmd)
    
@router.get("/{dog_id}/treats", response_model=List[GetTreatResponse])
async def get_treats_by_dog(
    *, dog_id: str, get_treats: GetTreatsByDogUseCase = Depends()
):
    return await get_treats(dog_id)

@router.get("/{dog_id}/treats/{treat_id}", response_model=GetTreatResponse)
async def get_treat(
    *, dog_id: str, treat_id: str, get_by_id: GetTreatUseCase = Depends()
):
    return await get_by_id(id=treat_id, dog_id=dog_id)

@router.patch("/{dog_id}/treats/{treat_id}", response_model=GetTreatResponse)
async def patch_treat(
    *,
    dog_id: str,
    treat_id: str,
    body: UpdateTreatRequest,
    update: UpdateTreatUseCase = Depends()
):
    cmd = UpdateTreatCommand(id=treat_id, dog_id=dog_id, **body.model_dump())
    return await update(cmd)

@router.delete("/{dog_id}/treats/{treat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_treat(
    *, dog_id: str, treat_id: str, delete: DeleteTreatUseCase = Depends()
):
    await delete(id=treat_id, dog_id=dog_id)