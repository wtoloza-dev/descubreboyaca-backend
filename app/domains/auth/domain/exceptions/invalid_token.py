"""Invalid token domain exception."""

from typing import Any

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class InvalidTokenException(AuthenticationException):
    """Exception raised when a JWT token is invalid.

    Raised when the token signature is invalid, token is malformed,
    or token cannot be decoded.

    Example:
        >>> raise InvalidTokenException(
        ...     reason="malformed_token",
        ... )
    """

    def __init__(
        self,
        reason: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize invalid token exception.

        Args:
            reason: Optional reason why token is invalid
            context: Additional context
        """
        full_context = {
            **({"reason": reason} if reason else {}),
            **(context or {}),
        }
        super().__init__(
            message="Invalid authentication token",
            context=full_context,
            error_code="INVALID_TOKEN",
        )
