from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.medicine_record.application.error.MedRecordNotFoundError import MedRecordNotFoundError
from app.medicine_record.application.error.MedRecordOwnershipError import MedRecordOwnershipError


async def medicine_record_not_found_handler(request: Request, exc: MedRecordNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


async def medicine_record_ownership_handler(request: Request, exc: MedRecordOwnershipError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


error_handlers = {
    MedRecordNotFoundError: medicine_record_not_found_handler,
    MedRecordOwnershipError: medicine_record_ownership_handler,
}
