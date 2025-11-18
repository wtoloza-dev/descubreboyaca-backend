"""Use case for toggling dish availability.

This module provides the business logic for enabling or disabling
a dish without deleting it.
"""

from app.domains.restaurants.domain import Dish, DishData
from app.domains.restaurants.domain.exceptions import DishNotFoundException
from app.domains.restaurants.domain.interfaces import DishRepositoryInterface


class ToggleDishAvailabilityUseCase:
    """Use case for toggling dish availability (soft enable/disable).

    This use case allows changing a dish's availability status without
    deleting or fully updating the dish.

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
        is_available: bool,
        updated_by: str | None = None,
    ) -> Dish:
        """Execute the toggle dish availability use case.

        Args:
            dish_id: ULID of the dish
            is_available: New availability status
            updated_by: ULID of the user making the change

        Returns:
            Dish: Updated dish

        Raises:
            DishNotFoundException: If dish is not found
        """
        # Get current dish (raises exception if not found)
        dish = await self.repository.get_by_id(dish_id)
        if not dish:
            raise DishNotFoundException(dish_id)

        # Update only is_available field
        dish_data = DishData(
            restaurant_id=dish.restaurant_id,
            name=dish.name,
            description=dish.description,
            category=dish.category,
            price=dish.price,
            original_price=dish.original_price,
            is_available=is_available,  # Toggle this
            preparation_time_minutes=dish.preparation_time_minutes,
            serves=dish.serves,
            calories=dish.calories,
            image_url=dish.image_url,
            dietary_restrictions=dish.dietary_restrictions,
            ingredients=dish.ingredients,
            allergens=dish.allergens,
            flavor_profile=dish.flavor_profile,
            is_featured=dish.is_featured,
            display_order=dish.display_order,
        )

        updated = await self.repository.update(
            dish_id, dish_data, updated_by=updated_by
        )

        if not updated:
            raise DishNotFoundException(dish_id)

        return updated
