"""Unauthorized exception.

This module defines the base exception for authentication errors.
"""

from typing import Any

from app.shared.domain.exceptions.domain_exception import DomainException


class UnauthorizedException(DomainException):
    """Exception raised when authentication is required or has failed.

    This is a base exception for all authentication errors across domains.
    Specific domain exceptions should inherit from this class.

    Example:
        >>> raise UnauthorizedException(
        ...     message="Invalid credentials for user 'user@example.com'",
        ...     context={"email": "user@example.com"},
        ...     error_code="INVALID_CREDENTIALS",
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "UNAUTHORIZED",
    ) -> None:
        """Initialize unauthorized exception.

        Args:
            message: Human-readable error message
            context: Additional context about the error
            error_code: Machine-readable error code
        """
        super().__init__(
            message=message,
            context=context,
            error_code=error_code,
        )
