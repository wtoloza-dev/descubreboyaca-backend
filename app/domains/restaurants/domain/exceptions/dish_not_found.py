"""Dish not found domain exception."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class DishNotFoundException(NotFoundException):
    """Exception raised when a dish is not found.

    This exception is raised when attempting to access a dish
    that doesn't exist in the system.

    Example:
        >>> raise DishNotFoundException(
        ...     dish_id="01HQ123ABC",
        ... )
    """

    def __init__(
        self,
        dish_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize dish not found exception.

        Args:
            dish_id: ULID of the dish that was not found
            context: Additional context
        """
        full_context = {
            "dish_id": dish_id,
            **(context or {}),
        }
        super().__init__(
            message=f"Dish with ID '{dish_id}' not found",
            context=full_context,
            error_code="DISH_NOT_FOUND",
        )

