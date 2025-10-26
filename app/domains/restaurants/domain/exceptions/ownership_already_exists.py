"""Ownership already exists exception.

This module defines the exception raised when attempting to create a duplicate ownership relationship.
"""

from app.shared.domain.exceptions.base import AlreadyExistsException


class OwnershipAlreadyExistsException(AlreadyExistsException):
    """Exception raised when attempting to create a duplicate ownership relationship.

    This exception is raised when an owner is already assigned to a restaurant.

    Example:
        >>> raise OwnershipAlreadyExistsException("01J9X...", "01J9Y...")
        OwnershipAlreadyExistsException: Owner '01J9Y...' is already assigned to restaurant '01J9X...'
    """

    def __init__(self, restaurant_id: str, owner_id: str) -> None:
        """Initialize ownership already exists exception.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner
        """
        self.restaurant_id = restaurant_id
        self.owner_id = owner_id
        super().__init__(
            entity_type="Ownership",
            identifier=f"Owner {owner_id} is already assigned to restaurant {restaurant_id}",
        )
