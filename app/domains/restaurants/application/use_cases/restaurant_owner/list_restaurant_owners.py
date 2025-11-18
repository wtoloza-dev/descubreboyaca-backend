"""Use case for listing all owners of a restaurant.

This module provides the business logic for retrieving all users
who have ownership or management roles for a specific restaurant.
"""

from app.domains.restaurants.domain.entities import RestaurantOwner
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class ListRestaurantOwnersUseCase:
    """Use case for listing all owners of a restaurant.

    This use case retrieves all ownership relationships for a restaurant,
    useful for displaying team members.

    Attributes:
        repository: Restaurant owner repository for data retrieval
    """

    def __init__(
        self,
        repository: RestaurantOwnerRepositoryInterface,
    ) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Restaurant owner repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        restaurant_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[RestaurantOwner]:
        """Execute the list restaurant owners use case.

        Args:
            restaurant_id: ULID of the restaurant
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of restaurant owners
        """
        return await self.repository.list_by_restaurant(restaurant_id, offset, limit)
