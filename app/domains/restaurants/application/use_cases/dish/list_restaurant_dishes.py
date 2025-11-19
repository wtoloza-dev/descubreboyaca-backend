"""Use case for listing dishes of a restaurant.

This module provides the business logic for retrieving all dishes
belonging to a specific restaurant with optional filters and pagination.
"""

from typing import Any

from app.domains.restaurants.domain import Dish
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.domain.interfaces import (
    DishRepositoryInterface,
    RestaurantRepositoryInterface,
)


class ListRestaurantDishesUseCase:
    """Use case for getting all dishes for a specific restaurant.

    This use case validates the restaurant exists and retrieves its dishes
    with optional filtering and pagination.

    Attributes:
        dish_repository: Dish repository for data retrieval
        restaurant_repository: Restaurant repository for validation
    """

    def __init__(
        self,
        dish_repository: DishRepositoryInterface,
        restaurant_repository: RestaurantRepositoryInterface,
    ) -> None:
        """Initialize the use case with dependencies.

        Args:
            dish_repository: Dish repository implementation
            restaurant_repository: Restaurant repository for validation
        """
        self.dish_repository = dish_repository
        self.restaurant_repository = restaurant_repository

    async def execute(
        self,
        restaurant_id: str,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Dish], int]:
        """Execute the list restaurant dishes use case.

        Args:
            restaurant_id: ULID of the restaurant
            filters: Optional filters (category, is_available, is_featured)
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of dishes, total count)

        Raises:
            RestaurantNotFoundException: If the restaurant doesn't exist
        """
        # Validate restaurant exists
        restaurant = await self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)

        # Get dishes with count in single operation
        return await self.dish_repository.find_with_count_by_restaurant_id(
            restaurant_id, filters=filters, offset=offset, limit=limit
        )
