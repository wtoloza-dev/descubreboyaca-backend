"""Invalid owner role domain exception."""

from typing import Any

from app.shared.domain.exceptions import ValidationException


class InvalidOwnerRoleException(ValidationException):
    """Exception raised when an invalid owner role is provided.

    This exception is raised when attempting to set a role
    that is not recognized by the system.

    Example:
        >>> raise InvalidOwnerRoleException(
        ...     role="invalid_role",
        ... )
    """

    def __init__(
        self,
        role: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize invalid owner role exception.

        Args:
            role: The invalid role value
            context: Additional context
        """
        full_context = {
            "role": role,
            "field": "role",
            "valid_values": ["PRIMARY", "SECONDARY", "STAFF"],
            **(context or {}),
        }
        super().__init__(
            message=f"Invalid role '{role}'. Must be one of: PRIMARY, SECONDARY, STAFF",
            context=full_context,
            error_code="INVALID_OWNER_ROLE",
        )
