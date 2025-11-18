"""Use case for verifying restaurant ownership.

This module provides the business logic for checking if a user
has ownership or management rights for a restaurant.
"""

from app.domains.restaurants.domain.entities import RestaurantOwner
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class VerifyOwnershipUseCase:
    """Use case for verifying that a user is an owner of a specific restaurant.

    This use case checks if an ownership relationship exists between
    a user and a restaurant.

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
        self, owner_id: str, restaurant_id: str
    ) -> RestaurantOwner | None:
        """Execute the verify ownership use case.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Returns:
            RestaurantOwner if user is an owner, None otherwise
        """
        return await self.repository.get_by_ids(restaurant_id, owner_id)
