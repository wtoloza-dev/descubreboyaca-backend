"""Use case for updating an existing dish.

This module provides the business logic for updating dish information.
"""

from app.domains.restaurants.domain import Dish, DishData
from app.domains.restaurants.domain.exceptions import DishNotFoundException
from app.domains.restaurants.domain.interfaces import DishRepositoryInterface


class UpdateDishUseCase:
    """Use case for updating an existing dish.

    This use case handles updating dish data and ensures
    the dish exists before updating.

    Attributes:
        repository: Dish repository for data persistence
    """

    def __init__(self, repository: DishRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Dish repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        dish_id: str,
        dish_data: DishData,
        updated_by: str | None = None,
    ) -> Dish:
        """Execute the update dish use case.

        Args:
            dish_id: ULID of the dish to update
            dish_data: Updated dish data
            updated_by: ULID of the user updating the dish

        Returns:
            Dish: Updated dish

        Raises:
            DishNotFoundException: If dish is not found
        """
        # Verify dish exists first
        existing_dish = await self.repository.get_by_id(dish_id)
        if not existing_dish:
            raise DishNotFoundException(dish_id)

        # Update dish
        updated = await self.repository.update(
            dish_id, dish_data, updated_by=updated_by
        )

        if not updated:
            raise DishNotFoundException(dish_id)

        return updated
