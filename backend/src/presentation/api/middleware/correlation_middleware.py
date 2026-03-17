# src/presentation/api/middleware/correlation_middleware.py

from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.infrastructure.logging.context import (
    set_correlation_id,
    get_correlation_id,
    clear_correlation_id,
)


class CorrelationIdMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        correlation_id = request.headers.get("X-Request-ID") or str(uuid4())
        set_correlation_id(correlation_id)

        try:
            response = await call_next(request)
        except Exception:
            # важно: не трогаем response
            raise
        else:
            response.headers["X-Request-ID"] = get_correlation_id() or ""
            return response
        finally:
            clear_correlation_id()
