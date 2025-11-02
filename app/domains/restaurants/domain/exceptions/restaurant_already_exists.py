"""Restaurant already exists domain exception."""

from typing import Any

from app.shared.domain.exceptions import AlreadyExistsException


class RestaurantAlreadyExistsException(AlreadyExistsException):
    """Exception raised when attempting to create a duplicate restaurant.

    This exception is raised when a restaurant with the same name
    already exists in the same location.

    Example:
        >>> raise RestaurantAlreadyExistsException(
        ...     restaurant_name="La Puerta de Alcalá",
        ... )
    """

    def __init__(
        self,
        restaurant_name: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize restaurant already exists exception.

        Args:
            restaurant_name: Name of the restaurant that already exists
            context: Additional context
        """
        full_context = {
            "restaurant_name": restaurant_name,
            **(context or {}),
        }
        super().__init__(
            message=f"Restaurant with name '{restaurant_name}' already exists",
            context=full_context,
            error_code="RESTAURANT_ALREADY_EXISTS",
        )
