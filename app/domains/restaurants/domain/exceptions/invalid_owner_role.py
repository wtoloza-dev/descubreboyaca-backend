"""Invalid owner role exception.

This module defines the exception raised when an invalid owner role is provided.
"""

from app.shared.domain.exceptions.base import ValidationException


class InvalidOwnerRoleException(ValidationException):
    """Exception raised when an invalid owner role is provided.

    This exception is raised when attempting to set a role
    that is not recognized by the system.

    Example:
        >>> raise InvalidOwnerRoleException("invalid_role")
        InvalidOwnerRoleException: Invalid role: 'invalid_role'. Must be one of: owner, manager, staff
    """

    def __init__(self, role: str) -> None:
        """Initialize invalid owner role exception.

        Args:
            role: The invalid role value
        """
        super().__init__(
            message=f"Invalid role '{role}'. Must be one of: owner, manager, staff",
            field="role",
            value=role,
        )
