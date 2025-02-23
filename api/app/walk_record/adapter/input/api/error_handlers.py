from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.walk_record.application.error.WalkRecordNotFoundError import WalkRecordNotFoundError
from app.walk_record.application.error.WalkRecordOwnershipError import WalkRecordOwnershipError


async def walk_record_not_found_handler(request: Request, exc: WalkRecordNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


async def walk_record_ownership_handler(request: Request, exc: WalkRecordOwnershipError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


error_handlers = {
    WalkRecordNotFoundError: walk_record_not_found_handler,
    WalkRecordOwnershipError: walk_record_ownership_handler,
}
