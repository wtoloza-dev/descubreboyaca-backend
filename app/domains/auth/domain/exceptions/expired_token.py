"""Expired token domain exception."""

from typing import Any

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class ExpiredTokenException(AuthenticationException):
    """Exception raised when a JWT token has expired.

    Raised when attempting to use a token that has passed its expiration time.

    Example:
        >>> raise ExpiredTokenException(
        ...     expired_at="2024-01-01T00:00:00Z",
        ... )
    """

    def __init__(
        self,
        expired_at: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize expired token exception.

        Args:
            expired_at: Optional timestamp when token expired
            context: Additional context
        """
        full_context = {
            **({"expired_at": expired_at} if expired_at else {}),
            **(context or {}),
        }
        super().__init__(
            message="Authentication token has expired",
            context=full_context,
            error_code="EXPIRED_TOKEN",
        )
