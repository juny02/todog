from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.dog.application.error.DogNotFoundError import DogNotFoundError
from app.dog_family.adapter.input.api.request.AddDogFamilyRequest import (
    AddDogFamilyRequest,
)
from app.dog_family.adapter.input.api.request.GetDogFamiliesRequest import (
    GetDogFamiliesRequest,
)
from app.dog_family.adapter.input.api.request.UpdateDogFamilyRequest import (
    UpdateDogFamilyRequest,
)
from app.dog_family.adapter.input.api.response.GetDogFamilyResponse import (
    GetDogFamilyResponse,
)
from app.dog_family.application.error.DogFamilyAlreadyExistsError import (
    DogFamilyAlreadyExistsError,
)
from app.dog_family.application.error.DogFamilyNotFoundError import (
    DogFamilyNotFoundError,
)
from app.dog_family.application.port.input.AddDogFamilyCommand import (
    AddDogFamilyCommand,
)
from app.dog_family.application.port.input.GetDogFamiliesCommand import (
    GetDogFamiliesCommand,
)
from app.dog_family.application.port.input.UpdateDogFamilyCommand import (
    UpdateDogFamilyCommand,
)
from app.dog_family.application.usecase.AddDogFamilyUseCase import AddDogFamilyUseCase
from app.dog_family.application.usecase.DeleteDogFamilyUseCase import (
    DeleteDogFamilyUseCase,
)
from app.dog_family.application.usecase.GetDogFamiliesUseCase import (
    GetDogFamiliesUseCase,
)
from app.dog_family.application.usecase.GetDogFamilyUseCase import GetDogFamilyUseCase
from app.dog_family.application.usecase.UpdateDogFamilyUseCase import (
    UpdateDogFamilyUseCase,
)
from app.user.application.error.UserNotFoundError import UserNotFoundError

router = APIRouter(prefix="/dog_families", tags=["DogFamily"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_dog_family(
    *, body: AddDogFamilyRequest, add_dog_family: AddDogFamilyUseCase = Depends()
):
    cmd = AddDogFamilyCommand(**body.model_dump())

    try:
        return await add_dog_family(cmd)
    except (DogNotFoundError, UserNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DogFamilyAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[GetDogFamilyResponse])
async def get_DogFamilies(
    *,
    query: GetDogFamiliesRequest = Depends(),
    get_all: GetDogFamiliesUseCase = Depends()
):
    cmd = GetDogFamiliesCommand(**query.model_dump())

    return await get_all(cmd)


@router.get("/{id}", response_model=GetDogFamilyResponse)
async def get_dog_family(*, id: str, get_by_id: GetDogFamilyUseCase = Depends()):
    try:
        DogFamily = await get_by_id(id)
        return DogFamily
    except DogFamilyNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{id}", response_model=GetDogFamilyResponse)
async def patch_dog_family(
    *, id: str, body: UpdateDogFamilyRequest, update: UpdateDogFamilyUseCase = Depends()
):
    cmd = UpdateDogFamilyCommand(id=id, **body.model_dump())
    try:
        DogFamily = await update(cmd)
        return DogFamily
    except (DogNotFoundError, UserNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DogFamilyNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_dog_family(*, id: str, delete: DeleteDogFamilyUseCase = Depends()):
    try:
        await delete(id)
    except DogFamilyNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
