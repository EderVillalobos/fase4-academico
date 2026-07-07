class AppError(Exception):
    """Base exception for the academic application."""


class ValidationError(AppError):
    """Raised when a field or business rule is invalid."""


class ClientError(AppError):
    """Raised when a client operation fails."""


class ServiceError(AppError):
    """Raised when a service operation fails."""


class ReservationError(AppError):
    """Raised when a reservation operation fails."""

