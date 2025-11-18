"""Use case for getting the primary owner of a restaurant.

This module provides the business logic for retrieving the primary owner
of a specific restaurant.
"""

from app.domains.restaurants.domain.entities import RestaurantOwner
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class GetPrimaryOwnerUseCase:
    """Use case for getting the primary owner of a restaurant.

    This use case retrieves the primary ownership relationship for a restaurant.

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

    async def execute(self, restaurant_id: str) -> RestaurantOwner | None:
        """Execute the get primary owner use case.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Primary RestaurantOwner if found, None otherwise
        """
        return await self.repository.get_primary_owner(restaurant_id)
