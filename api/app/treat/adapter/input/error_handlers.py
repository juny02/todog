from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.treat.application.error.TreatOwnershipError import TreatOwnershipError
from app.treat.application.error.TreatNotFoundError import TreatNotFoundError
from app.dog.application.error.DogNotFoundError import DogNotFoundError


async def treat_not_found_handler(request: Request, exc: TreatNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


async def treat_ownership_handler(request: Request, exc: TreatOwnershipError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


async def dog_not_found_handler(request: Request, exc: DogNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


error_handlers = {
    TreatNotFoundError: treat_not_found_handler,
    TreatOwnershipError: treat_ownership_handler,
    DogNotFoundError: dog_not_found_handler,
}
