# src/infrastructure/logging/logger.py

import logging
import sys

from src.infrastructure.config.settings import settings
from src.infrastructure.logging.json_formatter import JsonFormatter


def configure_logging() -> None:
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    if settings.app_env.lower() == "production":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
