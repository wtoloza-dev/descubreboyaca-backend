"""Use case for getting all owners of a restaurant.

This module provides the business logic for retrieving complete
ownership information for a specific restaurant.
"""

from app.domains.restaurants.domain.entities import RestaurantOwner
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class GetOwnersByRestaurantUseCase:
    """Use case for getting all owners/team members of a specific restaurant.

    This use case retrieves all ownership relationships for a restaurant,
    useful for listing team members.

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

    async def execute(self, restaurant_id: str) -> list[RestaurantOwner]:
        """Execute the get owners by restaurant use case.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            List of owners/team members for the restaurant
        """
        return await self.repository.get_owners_by_restaurant(restaurant_id)
