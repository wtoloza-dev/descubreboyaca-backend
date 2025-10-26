"""Authentication exception.

This module defines the base authentication exception.
"""

from app.shared.domain.exceptions import DomainException


class AuthenticationException(DomainException):
    """Base exception for authentication errors.

    This is the base class for all authentication-related exceptions.
    """

    def __init__(
        self,
        error_code: str = "AUTHENTICATION_FAILED",
        message: str = "Authentication failed",
        context: dict[str, str] | None = None,
    ) -> None:
        """Initialize authentication exception.

        Args:
            error_code: Machine-readable error code
            message: Human-readable error message
            context: Additional error context
        """
        super().__init__(error_code=error_code, message=message, context=context)
