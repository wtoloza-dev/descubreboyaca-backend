"""Use case for creating a new dish.

This module provides the business logic for creating a dish entity
with restaurant validation.
"""

from app.domains.restaurants.domain.entities import Dish, DishData
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.domain.interfaces import (
    DishRepositoryInterface,
    RestaurantRepositoryInterface,
)


class CreateDishUseCase:
    """Use case for creating a new dish for a restaurant.

    This use case validates that the restaurant exists before creating
    the dish, ensuring referential integrity.

    Attributes:
        dish_repository: Dish repository for data persistence
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
        dish_data: DishData,
        restaurant_id: str,
        created_by: str | None = None,
    ) -> Dish:
        """Execute the create dish use case.

        Args:
            dish_data: Dish data without system metadata
            restaurant_id: ULID of the restaurant this dish belongs to
            created_by: ULID of the user creating the dish

        Returns:
            Dish: Created dish with ID and metadata

        Raises:
            RestaurantNotFoundException: If the restaurant doesn't exist
        """
        # Validate restaurant exists
        restaurant = await self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)

        # Create dish
        return await self.dish_repository.create(
            dish_data, restaurant_id=restaurant_id, created_by=created_by
        )
