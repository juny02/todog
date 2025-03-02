from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.medicine_schedule.application.error.MedScheduleNotFoundError import (
    MedScheduleNotFoundError,
)
from app.medicine_schedule.application.error.MedScheduleOwnershipError import (
    MedScheduleOwnershipError,
)


async def medicine_schedule_not_found_handler(request: Request, exc: MedScheduleNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


async def medicine_schedule_ownership_handler(request: Request, exc: MedScheduleOwnershipError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


error_handlers = {
    MedScheduleNotFoundError: medicine_schedule_not_found_handler,
    MedScheduleOwnershipError: medicine_schedule_ownership_handler,
}
