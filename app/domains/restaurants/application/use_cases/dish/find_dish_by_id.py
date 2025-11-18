"""Use case for finding a dish by its ID.

This module provides the business logic for retrieving a dish by its unique identifier.
"""

from app.domains.restaurants.domain import Dish
from app.domains.restaurants.domain.exceptions import DishNotFoundException
from app.domains.restaurants.domain.interfaces import DishRepositoryInterface


class FindDishByIdUseCase:
    """Use case for finding a dish by its ID.

    This use case retrieves a dish from the repository and ensures
    it exists, raising an exception if not found.

    Attributes:
        repository: Dish repository for data retrieval
    """

    def __init__(self, repository: DishRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Dish repository implementation
        """
        self.repository = repository

    async def execute(self, dish_id: str) -> Dish:
        """Execute the find dish by ID use case.

        Args:
            dish_id: ULID of the dish

        Returns:
            Dish: The found dish

        Raises:
            DishNotFoundException: If dish is not found
        """
        dish = await self.repository.get_by_id(dish_id)
        if not dish:
            raise DishNotFoundException(dish_id)
        return dish
