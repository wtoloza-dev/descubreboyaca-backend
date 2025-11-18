"""Use case for finding a restaurant by its ID.

This module provides the business logic for retrieving a restaurant by its unique identifier.
"""

from app.domains.restaurants.domain import Restaurant
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface


class FindRestaurantByIdUseCase:
    """Use case for finding a restaurant by its ID.

    This use case retrieves a restaurant from the repository and ensures
    it exists, raising an exception if not found.

    Attributes:
        repository: Restaurant repository for data retrieval
    """

    def __init__(self, repository: RestaurantRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Restaurant repository implementation
        """
        self.repository = repository

    async def execute(self, restaurant_id: str) -> Restaurant:
        """Execute the find restaurant by ID use case.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Restaurant: The found restaurant

        Raises:
            RestaurantNotFoundException: If restaurant is not found
        """
        restaurant = await self.repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)
        return restaurant
