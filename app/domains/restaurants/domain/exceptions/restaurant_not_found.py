"""Restaurant not found domain exception."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class RestaurantNotFoundException(NotFoundException):
    """Exception raised when a restaurant is not found.

    This exception is raised when attempting to access a restaurant
    that doesn't exist in the system.

    Example:
        >>> raise RestaurantNotFoundException(
        ...     restaurant_id="01HQ123ABC",
        ... )
    """

    def __init__(
        self,
        restaurant_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize restaurant not found exception.

        Args:
            restaurant_id: ULID of the restaurant that was not found
            context: Additional context
        """
        full_context = {
            "restaurant_id": restaurant_id,
            **(context or {}),
        }
        super().__init__(
            message=f"Restaurant with ID '{restaurant_id}' not found",
            context=full_context,
            error_code="RESTAURANT_NOT_FOUND",
        )
