"""Use case for checking if a user is an owner of a restaurant.

This module provides the business logic for a boolean ownership check.
"""

from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class CheckIsOwnerUseCase:
    """Use case for checking if a user is an owner of a specific restaurant.

    This is a convenience use case that returns a boolean instead of
    the ownership relationship entity.

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

    async def execute(self, owner_id: str, restaurant_id: str) -> bool:
        """Execute the check is owner use case.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Returns:
            True if user is an owner, False otherwise
        """
        return await self.repository.is_owner_of_restaurant(owner_id, restaurant_id)
