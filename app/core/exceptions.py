from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


class AppErrorException(Exception):
    """Base exception for application"""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def value_error_handler(request: Request, exc: ValueError):  # noqa: ARG001
    """Handle value exceptions"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):  # noqa: ARG001
    """Handle validation exceptions"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": [str(exc) for exc in exc.errors()]},
    )


async def http_error_handler(request: Request, exc: HTTPException):  # noqa: ARG001
    """Handle HTTP exception"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def app_error_handler(request: Request, exc: AppErrorException):  # noqa: ARG001
    """Handle App exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
