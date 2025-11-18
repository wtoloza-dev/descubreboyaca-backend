"""Use case for creating a new restaurant.

This module provides the business logic for creating a restaurant entity.
"""

from app.domains.restaurants.domain import Restaurant, RestaurantData
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface


class CreateRestaurantUseCase:
    """Use case for creating a new restaurant.

    This use case handles the creation of a new restaurant in the system,
    delegating the persistence to the repository.

    Attributes:
        repository: Restaurant repository for data persistence
    """

    def __init__(self, repository: RestaurantRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Restaurant repository implementation
        """
        self.repository = repository

    async def execute(
        self, restaurant_data: RestaurantData, created_by: str | None = None
    ) -> Restaurant:
        """Execute the create restaurant use case.

        Args:
            restaurant_data: Restaurant data without system metadata
            created_by: ULID of the user creating the restaurant

        Returns:
            Restaurant: Created restaurant with ID and metadata
        """
        return await self.repository.create(restaurant_data, created_by=created_by)
