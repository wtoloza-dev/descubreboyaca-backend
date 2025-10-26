"""Restaurant not found exception.

This module defines the exception raised when a restaurant is not found.
"""

from app.shared.domain.exceptions.base import NotFoundException


class RestaurantNotFoundException(NotFoundException):
    """Exception raised when a restaurant is not found.

    This exception is raised when attempting to access a restaurant
    that doesn't exist in the system.

    Example:
        >>> raise RestaurantNotFoundException("01J9X...")
        RestaurantNotFoundException: Restaurant with ID '01J9X...' not found
    """

    def __init__(self, restaurant_id: str) -> None:
        """Initialize restaurant not found exception.

        Args:
            restaurant_id: ULID of the restaurant that was not found
        """
        super().__init__(entity_type="Restaurant", entity_id=restaurant_id)
