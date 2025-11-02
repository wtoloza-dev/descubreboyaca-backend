"""Invalid credentials domain exception."""

from typing import Any

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class InvalidCredentialsException(AuthenticationException):
    """Exception raised when user credentials are invalid.

    Raised when the email/password combination doesn't match any registered
    user or when the provided credentials are incorrect.

    Example:
        >>> raise InvalidCredentialsException(
        ...     email="user@example.com",
        ... )
    """

    def __init__(
        self,
        email: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize invalid credentials exception.

        Args:
            email: Optional email that failed authentication
            context: Additional context
        """
        full_context = {
            **({"email": email} if email else {}),
            **(context or {}),
        }
        super().__init__(
            message="Invalid email or password",
            context=full_context,
            error_code="INVALID_CREDENTIALS",
        )
