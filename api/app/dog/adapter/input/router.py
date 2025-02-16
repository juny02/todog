from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.dog.adapter.input.api.request.GetDogsRequest import GetDogsRequest
from app.dog.adapter.input.api.request.UpdateDogRequest import UpdateDogRequest
from app.dog.adapter.input.api.response.GetDogResponse import GetDogResponse
from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog.application.port.input.CreateDogCommand import CreateDogCommand
from app.dog.application.usecase.DeleteDogUseCase import DeleteDogUseCase
from app.dog.application.usecase.GetDogUseCase import GetDogUseCase
from app.dog.application.usecase.CreateDogUseCase import CreateDogUseCase
from app.dog.application.usecase.GetDogsUseCase import GetDogsUseCase
from app.dog.application.usecase.CreateDogUseCase import CreateDogUseCase
from app.dog.application.port.input.UpdateDogCommand import UpdateDogCommand
from app.dog.application.port.input.GetDogsCommand import GetDogsCommand
from app.dog.application.usecase.UpdateDogUseCase import UpdateDogUseCase
from app.dog.adapter.input.api.request.CreateDogRequest import CreateDogRequest


router = APIRouter(prefix="/dogs", tags=["Dog"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_dog(*, body: CreateDogRequest, create_dog: CreateDogUseCase = Depends()):
    cmd = CreateDogCommand(**body.model_dump())

    return await create_dog(cmd)


@router.get("", response_model=List[GetDogResponse])
async def get_dogs(
    *, query: GetDogsRequest = Depends(), get_all: GetDogsUseCase = Depends()
):
    cmd = GetDogsCommand(**query.model_dump())

    return await get_all(cmd)


@router.get("/{id}", response_model=GetDogResponse)
async def get_dog(*, id: str, get_by_id: GetDogUseCase = Depends()):
    try:
        dog = await get_by_id(id)
        return dog
    except DogNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



@router.patch("/{id}", response_model=GetDogResponse)
async def patch_dog(
    *, id: str, body: UpdateDogRequest, update: UpdateDogUseCase = Depends()
):
    cmd = UpdateDogCommand(id=id, **body.model_dump())
    try:
        dog = await update(cmd)
        return dog
    except DogNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_dog(*, id: str, delete: DeleteDogUseCase = Depends()):
    try:
        await delete(id)
    except DogNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
