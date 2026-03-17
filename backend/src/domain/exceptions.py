# src/domain/exceptions.py


class DomainError(Exception):
    """Base exception for domain layer."""


class ValidationError(DomainError):
    """Raised when input data is invalid."""


class SingularMatrixError(DomainError):
    """Raised when the system cannot be solved due to numerical instability."""


class GammaStrategyError(DomainError):
    """Raised when gamma cannot be computed."""
