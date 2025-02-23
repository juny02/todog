from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.meal_record.application.error.MealRecordNotFoundError import MealRecordNotFoundError
from app.meal_record.application.error.MealRecordOwnershipError import MealRecordOwnershipError


async def meal_record_not_found_handler(request: Request, exc: MealRecordNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


async def meal_record_ownership_handler(request: Request, exc: MealRecordOwnershipError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


error_handlers = {
    MealRecordNotFoundError: meal_record_not_found_handler,
    MealRecordOwnershipError: meal_record_ownership_handler,
}
