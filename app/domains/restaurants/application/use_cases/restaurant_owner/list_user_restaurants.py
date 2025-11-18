"""Use case for listing all restaurants owned by a user.

This module provides the business logic for retrieving all restaurants
that a user owns or manages.
"""

from app.domains.restaurants.domain.entities import RestaurantOwner
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class ListUserRestaurantsUseCase:
    """Use case for listing all restaurants owned by a user.

    This use case retrieves all ownership relationships for a user,
    useful for displaying "My Restaurants".

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
        owner_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[RestaurantOwner]:
        """Execute the list user restaurants use case.

        Args:
            owner_id: ULID of the owner
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of restaurant ownerships for the user
        """
        return await self.repository.list_by_owner(owner_id, offset, limit)
