from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.schedule.application.error.ScheduleNotFoundError import ScheduleNotFoundError
from app.schedule.application.error.ScheduleOwnershipError import ScheduleOwnershipError


async def schedule_not_found_handler(request: Request, exc: ScheduleNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


async def schedule_ownership_handler(request: Request, exc: ScheduleOwnershipError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


error_handlers = {
    ScheduleNotFoundError: schedule_not_found_handler,
    ScheduleOwnershipError: schedule_ownership_handler,
}
