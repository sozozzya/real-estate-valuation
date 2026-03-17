# src/infrastructure/logging/context.py

import contextvars
import uuid

_correlation_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "correlation_id",
    default=None,
)


def set_correlation_id(correlation_id: str | None = None) -> None:
    _correlation_id.set(correlation_id or str(uuid.uuid4()))


def get_correlation_id() -> str | None:
    return _correlation_id.get()


def clear_correlation_id() -> None:
    _correlation_id.set(None)
