"""Use case for listing all dishes with filters.

This module provides the business logic for retrieving dishes
with optional filtering and pagination.
"""

from typing import Any

from app.domains.restaurants.domain import Dish
from app.domains.restaurants.domain.interfaces import DishRepositoryInterface


class ListDishesUseCase:
    """Use case for listing all dishes with optional filters and pagination.

    This use case allows searching and filtering dishes across all restaurants
    with pagination support.

    Attributes:
        repository: Dish repository for data retrieval
    """

    def __init__(self, repository: DishRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Dish repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Dish], int]:
        """Execute the list dishes use case.

        Args:
            filters: Optional filters (restaurant_id, category, is_available, etc.)
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of dishes, total count)
        """
        dishes = await self.repository.find(filters=filters, offset=offset, limit=limit)

        total_count = await self.repository.count(filters=filters)

        return dishes, total_count
