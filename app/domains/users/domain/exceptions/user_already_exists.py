"""User already exists domain exception."""

from typing import Any

from app.shared.domain.exceptions import AlreadyExistsException


class UserAlreadyExistsException(AlreadyExistsException):
    """Exception raised when attempting to create a user that already exists.

    Raised when registering with an email address that's already registered
    in the system.

    Example:
        >>> raise UserAlreadyExistsException(
        ...     email="user@example.com",
        ... )
    """

    def __init__(
        self,
        email: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize user already exists exception.

        Args:
            email: Email address that already exists
            context: Additional context
        """
        full_context = {
            "email": email,
            **(context or {}),
        }
        super().__init__(
            message=f"User with email '{email}' already exists",
            context=full_context,
            error_code="USER_ALREADY_EXISTS",
        )
