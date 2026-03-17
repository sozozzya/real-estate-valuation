# src/presentation/main.py

from fastapi import FastAPI
from src.presentation.api.routes import router
from src.presentation.health import router as health_router
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config.settings import settings
from src.infrastructure.logging.logger import configure_logging
from src.presentation.api.exception_handlers import register_exception_handlers
from src.presentation.api.middleware.correlation_middleware import (
    CorrelationIdMiddleware,
)
from src.presentation.api.middleware.logging_middleware import LoggingMiddleware


def create_app():
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_env == "development",
        version="1.0.0",
    )

    # === Middleware ===
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # можно ограничить позже
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(LoggingMiddleware)

    # === Exception handlers ===
    register_exception_handlers(app)

    # === Routes ===
    app.include_router(health_router)
    app.include_router(router, prefix="/api", tags=["Ridge"])

    return app


app = create_app()
