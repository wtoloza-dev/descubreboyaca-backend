"""Cannot remove primary owner exception.

This module defines the exception raised when attempting to remove the primary owner.
"""

from app.shared.domain.exceptions.base import ValidationException


class CannotRemovePrimaryOwnerException(ValidationException):
    """Exception raised when attempting to remove the primary owner.

    This exception is raised when trying to remove a primary owner
    without transferring ownership first.

    Example:
        >>> raise CannotRemovePrimaryOwnerException("01J9Y...")
        CannotRemovePrimaryOwnerException: Cannot remove primary owner without transferring ownership first
    """

    def __init__(self, owner_id: str) -> None:
        """Initialize cannot remove primary owner exception.

        Args:
            owner_id: ULID of the primary owner being removed
        """
        super().__init__(
            message="Cannot remove primary owner. Transfer ownership first or assign a new primary owner.",
            field="is_primary",
            value=owner_id,
        )
