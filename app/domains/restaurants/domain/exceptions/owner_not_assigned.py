"""Owner not assigned exception.

This module defines the exception raised when attempting to transfer ownership to an unassigned user.
"""

from app.shared.domain.exceptions.base import ValidationException


class OwnerNotAssignedException(ValidationException):
    """Exception raised when attempting to transfer ownership to an unassigned user.

    This exception is raised when trying to make someone primary owner
    who is not yet assigned to the restaurant.

    Example:
        >>> raise OwnerNotAssignedException("01J9X...", "01J9Y...")
        OwnerNotAssignedException: Owner must be assigned to restaurant before transferring ownership
    """

    def __init__(self, restaurant_id: str, owner_id: str) -> None:
        """Initialize owner not assigned exception.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner
        """
        self.restaurant_id = restaurant_id
        self.owner_id = owner_id
        super().__init__(
            message=f"Owner {owner_id} must be assigned to restaurant {restaurant_id} before transferring ownership",
            field="owner_id",
            value=owner_id,
        )
