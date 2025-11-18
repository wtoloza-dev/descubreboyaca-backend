"""Use case for counting restaurants with filters.

This module provides the business logic for counting restaurants
that match specific criteria.
"""

from typing import Any

from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface


class CountRestaurantsUseCase:
    """Use case for counting restaurants with dynamic filters.

    This use case allows counting restaurants that match various filters,
    useful for pagination and statistics.

    Attributes:
        repository: Restaurant repository for data retrieval
    """

    def __init__(self, repository: RestaurantRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Restaurant repository implementation
        """
        self.repository = repository

    async def execute(self, filters: dict[str, Any] | None = None) -> int:
        """Execute the count restaurants use case.

        Args:
            filters: Dictionary of field names and their values to filter by

        Returns:
            Count of restaurants matching the filters

        Example:
            >>> total = await use_case.execute()
            >>> total = await use_case.execute({"city": "Tunja"})
            >>> total = await use_case.execute({"city": "Tunja", "price_level": 2})
        """
        return await self.repository.count(filters=filters)
