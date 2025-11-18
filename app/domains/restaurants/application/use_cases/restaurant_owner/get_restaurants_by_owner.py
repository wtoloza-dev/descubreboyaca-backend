"""Use case for getting all restaurants owned by a user.

This module provides the business logic for retrieving complete
restaurant ownership information for a specific user.
"""

from app.domains.restaurants.domain.entities import RestaurantOwner
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class GetRestaurantsByOwnerUseCase:
    """Use case for getting all restaurants owned by a specific user.

    This use case retrieves all restaurant ownership relationships
    for a given user, useful for listing "My Restaurants".

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

    async def execute(self, owner_id: str) -> list[RestaurantOwner]:
        """Execute the get restaurants by owner use case.

        Args:
            owner_id: ULID of the owner

        Returns:
            List of restaurant ownerships for the user
        """
        return await self.repository.get_restaurants_by_owner(owner_id)
