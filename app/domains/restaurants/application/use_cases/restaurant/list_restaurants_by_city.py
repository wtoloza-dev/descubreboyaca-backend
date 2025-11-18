"""Use case for listing restaurants by city.

This module provides the business logic for retrieving restaurants
in a specific city with pagination.
"""

from app.domains.restaurants.domain import Restaurant
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface


class ListRestaurantsByCityUseCase:
    """Use case for listing restaurants by city.

    This use case retrieves restaurants filtered by city with pagination support.

    Attributes:
        repository: Restaurant repository for data retrieval
    """

    def __init__(self, repository: RestaurantRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Restaurant repository implementation
        """
        self.repository = repository

    async def execute(
        self, city: str, offset: int = 0, limit: int = 20
    ) -> tuple[list[Restaurant], int]:
        """Execute the list restaurants by city use case.

        Args:
            city: City name to filter by
            offset: Number of records to offset
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of restaurants in the city, total count)
        """
        restaurants = await self.repository.find(
            filters={"city": city}, offset=offset, limit=limit
        )
        total = await self.repository.count(filters={"city": city})
        return restaurants, total
