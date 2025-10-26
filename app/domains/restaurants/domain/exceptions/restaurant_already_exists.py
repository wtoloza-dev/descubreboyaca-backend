"""Restaurant already exists exception.

This module defines the exception raised when attempting to create a duplicate restaurant.
"""

from app.shared.domain.exceptions.base import AlreadyExistsException


class RestaurantAlreadyExistsException(AlreadyExistsException):
    """Exception raised when attempting to create a duplicate restaurant.

    This exception is raised when a restaurant with the same name
    already exists in the system.

    Example:
        >>> raise RestaurantAlreadyExistsException("La Puerta de Alcalá")
        RestaurantAlreadyExistsException: Restaurant with identifier 'La Puerta de Alcalá' already exists
    """

    def __init__(self, restaurant_name: str) -> None:
        """Initialize restaurant already exists exception.

        Args:
            restaurant_name: Name of the restaurant that already exists
        """
        super().__init__(entity_type="Restaurant", identifier=restaurant_name)
