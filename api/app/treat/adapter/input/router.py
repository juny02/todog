from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.treat.adapter.input.api.request.CreateTreatRequest import CreateTreatRequest
from app.treat.adapter.input.api.request.UpdateTreatRequest import UpdateTreatRequest
from app.treat.adapter.input.api.response.GetTreatResponse import GetTreatResponse
from app.treat.application.error.TreatNotFoundError import TreatNotFoundError
from app.treat.application.port.input.CreateTreatCommand import CreateTreatCommand
from app.treat.application.port.input.UpdateTreatCommand import UpdateTreatCommand
from app.treat.application.usecase.CreateTreatUseCase import CreateTreatUseCase
from app.treat.application.usecase.DeleteTreatUseCase import DeleteTreatUseCase
from app.treat.application.usecase.GetTreatsByDogUseCase import GetTreatsByDogUseCase
from app.treat.application.usecase.GetTreatUseCase import GetTreatUseCase
from app.treat.application.usecase.UpdateTreatUseCase import UpdateTreatUseCase

# 강아지 별 간식 관리 라우터
dog_treat_router = APIRouter(prefix="/dogs", tags=["Dog Treats"])

@dog_treat_router.post("/{dog_id}/treats", status_code=status.HTTP_201_CREATED)
async def post_treat(
    *, dog_id: str, body: CreateTreatRequest, create_treat: CreateTreatUseCase = Depends()
):
    cmd = CreateTreatCommand(dog_id=dog_id, **body.model_dump())
    try:
        return await create_treat(cmd)
    except DogNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@dog_treat_router.get("/{dog_id}/treats", response_model=List[GetTreatResponse])
async def get_treats_by_dog(
    *, dog_id: str, get_treats: GetTreatsByDogUseCase = Depends()
):
    return await get_treats(dog_id)


# 개별 간식 관리 라우터
treat_router = APIRouter(prefix="/treats", tags=["Treats"])

@treat_router.get("/{treat_id}", response_model=GetTreatResponse)
async def get_treat(*, treat_id: str, get_by_id: GetTreatUseCase = Depends()):
    try:
        return await get_by_id(treat_id)
    except TreatNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@treat_router.patch("/{treat_id}", response_model=GetTreatResponse)
async def patch_treat(
    *, treat_id: str, body: UpdateTreatRequest, update: UpdateTreatUseCase = Depends()
):
    cmd = UpdateTreatCommand(id=treat_id, **body.model_dump())
    try:
        return await update(cmd)
    except TreatNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@treat_router.delete("/{treat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_treat(*, treat_id: str, delete: DeleteTreatUseCase = Depends()):
    try:
        await delete(treat_id)
    except TreatNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# router = APIRouter(prefix="/treats", tags=["Treat"])


# @router.post("", status_code=status.HTTP_201_CREATED)
# async def post_treat(*, body: CreateTreatRequest, create_treat: CreateTreatUseCase = Depends()):
#     cmd = CreateTreatCommand(**body.model_dump())

#     return await create_treat(cmd)


# @router.get("/id?", response_model=List[GetTreatResponse])
# async def get_treats_by_dog(
#     *, get_treats: GetTreatsByDogUseCase = Depends()
# ):

#     return await get_treats(dog_id)


# @router.get("/{id}", response_model=GetTreatResponse)
# async def get_treat(*, id: str, get_by_id: GetTreatUseCase = Depends()):
#     try:
#         treat = await get_by_id(id)
#         return treat
#     except TreatNotFoundError as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



# @router.patch("/{id}", response_model=GetTreatResponse)
# async def patch_treat(
#     *, id: str, body: UpdateTreatRequest, update: UpdateTreatUseCase = Depends()
# ):
#     cmd = UpdateTreatCommand(id=id, **body.model_dump())
#     try:
#         treat = await update(cmd)
#         return treat
#     except TreatNotFoundError as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# @router.delete(
#     "/{id}",
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_treat(*, id: str, delete: DeleteTreatUseCase = Depends()):
#     try:
#         await delete(id)
#     except TreatNotFoundError as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
