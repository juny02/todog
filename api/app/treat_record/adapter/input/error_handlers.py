from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.treat_record.application.error.TreatRecordNotFoundError import TreatRecordNotFoundError
from app.treat_record.application.error.TreatRecordOwnershipError import TreatRecordOwnershipError


async def treat_record_not_found_handler(request: Request, exc: TreatRecordNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


async def treat_record_ownership_handler(request: Request, exc: TreatRecordOwnershipError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


error_handlers = {
    TreatRecordNotFoundError: treat_record_not_found_handler,
    TreatRecordOwnershipError: treat_record_ownership_handler,
}
