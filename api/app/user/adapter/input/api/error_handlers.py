from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.user.application.error.UserNotFoundError import UserNotFoundError


async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


error_handlers = {
    UserNotFoundError: user_not_found_handler
}
