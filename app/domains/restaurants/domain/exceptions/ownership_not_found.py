"""Ownership not found exception.

This module defines the exception raised when an ownership relationship is not found.
"""

from app.shared.domain.exceptions.base import NotFoundException


class OwnershipNotFoundException(NotFoundException):
    """Exception raised when an ownership relationship is not found.

    This exception is raised when attempting to access an ownership
    relationship that doesn't exist in the system.

    Example:
        >>> raise OwnershipNotFoundException("01J9X...", "01J9Y...")
        OwnershipNotFoundException: Ownership relationship not found for restaurant '01J9X...' and owner '01J9Y...'
    """

    def __init__(self, restaurant_id: str, owner_id: str) -> None:
        """Initialize ownership not found exception.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner
        """
        super().__init__(
            entity_type="Ownership",
            entity_id=f"restaurant: {restaurant_id}, owner: {owner_id}",
        )
