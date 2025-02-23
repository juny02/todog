from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.memo.application.error.MemoNotFoundError import MemoNotFoundError
from app.memo.application.error.MemoOwnershipError import MemoOwnershipError


async def memo_not_found_handler(request: Request, exc: MemoNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)})


async def memo_ownership_handler(request: Request, exc: MemoOwnershipError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)})


error_handlers = {
    MemoNotFoundError: memo_not_found_handler,
    MemoOwnershipError: memo_ownership_handler,
}
