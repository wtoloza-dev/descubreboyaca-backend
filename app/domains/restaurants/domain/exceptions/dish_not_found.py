"""Dish not found exception.

This module defines the exception raised when a dish is not found.
"""

from app.shared.domain.exceptions.base import NotFoundException


class DishNotFoundException(NotFoundException):
    """Exception raised when a dish is not found.

    This exception is raised when attempting to access a dish
    that doesn't exist in the system.

    Example:
        >>> raise DishNotFoundException("01J9X...")
        DishNotFoundException: Dish with ID '01J9X...' not found
    """

    def __init__(self, dish_id: str) -> None:
        """Initialize dish not found exception.

        Args:
            dish_id: ULID of the dish that was not found
        """
        super().__init__(entity_type="Dish", entity_id=dish_id)

