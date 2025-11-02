"""Authentication domain exception."""

from typing import Any

from app.shared.domain.exceptions import DomainException


class AuthenticationException(DomainException):
    """Base exception for authentication and authorization errors.

    This is the base class for all authentication-related exceptions
    in the auth domain (credentials, tokens, permissions, etc.).

    Example:
        >>> raise AuthenticationException(
        ...     message="Authentication failed",
        ...     context={"reason": "invalid_token"},
        ... )
    """

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str = "AUTHENTICATION_FAILED",
    ) -> None:
        """Initialize authentication exception.

        Args:
            message: Human-readable error message
            context: Additional error context
            error_code: Machine-readable error code
        """
        super().__init__(
            message=message,
            context=context,
            error_code=error_code,
        )
