"""User not found domain exception."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class UserNotFoundException(NotFoundException):
    """Exception raised when a user is not found.

    Raised when attempting to access or authenticate a user that doesn't exist
    in the system.

    Example:
        >>> raise UserNotFoundException(
        ...     identifier="user@example.com",
        ... )
    """

    def __init__(
        self,
        identifier: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize user not found exception.

        Args:
            identifier: User identifier (email or ID) that was not found
            context: Additional context
        """
        full_context = {
            "identifier": identifier,
            **(context or {}),
        }
        super().__init__(
            message=f"User '{identifier}' not found",
            context=full_context,
            error_code="USER_NOT_FOUND",
        )
