"""Use case for finding restaurants with filters and pagination.

This module provides the business logic for searching restaurants with
dynamic filters and pagination support.
"""

from typing import Any

from app.domains.restaurants.domain import Restaurant
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface


class FindRestaurantsUseCase:
    """Use case for finding restaurants with dynamic filters and pagination.

    This use case allows flexible restaurant searching with various filters
    and returns both results and total count for pagination.

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
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Restaurant], int]:
        """Execute the find restaurants use case.

        Args:
            filters: Dictionary of field names and their values to filter by
            offset: Number of records to offset
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of restaurants, total count)

        Example:
            >>> restaurants, total = await use_case.execute()
            >>> restaurants, total = await use_case.execute({"city": "Tunja"})
            >>> restaurants, total = await use_case.execute(
            ...     {"city": "Tunja", "price_level": 2}, offset=0, limit=10
            ... )
        """
        return await self.repository.find_with_count(
            filters=filters, offset=offset, limit=limit
        )
