# src/presentation/api/middleware/logging_middleware.py

import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.infrastructure.config.settings import settings
from src.infrastructure.logging.context import get_correlation_id

logger = logging.getLogger("http")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        if settings.log_requests:
            start_time = time.time()

            logger.info(
                "request_started",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "correlation_id": get_correlation_id(),
                },
            )

        response = await call_next(request)

        if settings.log_requests:
            duration = round((time.time() - start_time) * 1000, 2)

            logger.info(
                "request_completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration,
                    "correlation_id": get_correlation_id(),
                },
            )

        return response
