# src/presentation/api/exception_handlers.py

import logging
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.domain.exceptions import DomainError

logger = logging.getLogger("api.errors")


def _sanitize_for_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _sanitize_for_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize_for_json(v) for v in value]
    if isinstance(value, tuple):
        return [_sanitize_for_json(v) for v in value]
    if isinstance(value, BaseException):
        return str(value)
    return value


def register_exception_handlers(app):

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):

        logger.warning(
            "domain_error",
            extra={
                "path": request.url.path,
                "method": request.method,
                "client": request.client.host if request.client else None,
                "error": str(exc),
            },
        )

        return JSONResponse(
            status_code=400,
            content={
                "error": "DomainError",
                "message": str(exc),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        serialized_errors = _sanitize_for_json(exc.errors())

        logger.warning(
            "validation_error",
            extra={
                "path": request.url.path,
                "method": request.method,
                "client": request.client.host if request.client else None,
                "details": serialized_errors,
            },
        )

        return JSONResponse(
            status_code=422,
            content={
                "error": "ValidationError",
                "message": "Invalid request payload.",
                "details": serialized_errors,
            },
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception):

        logger.exception(
            "unexpected_error",
            extra={
                "path": request.url.path,
                "method": request.method,
                "client": request.client.host if request.client else None,
            },
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "Unexpected error occurred.",
            },
        )
