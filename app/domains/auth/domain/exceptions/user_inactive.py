"""User inactive domain exception."""

from typing import Any

from app.domains.auth.domain.exceptions.authentication import AuthenticationException


class UserInactiveException(AuthenticationException):
    """Exception raised when attempting to authenticate an inactive user.

    Raised when a user account has been deactivated or suspended and
    cannot be used for authentication.

    Example:
        >>> raise UserInactiveException(
        ...     email="user@example.com",
        ... )
    """

    def __init__(
        self,
        email: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize user inactive exception.

        Args:
            email: Email of the inactive user
            context: Additional context
        """
        full_context = {
            "email": email,
            **(context or {}),
        }
        super().__init__(
            message=f"User account '{email}' is inactive",
            context=full_context,
            error_code="USER_INACTIVE",
        )
