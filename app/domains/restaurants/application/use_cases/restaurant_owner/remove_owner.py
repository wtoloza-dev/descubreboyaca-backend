"""Use case for removing an owner from a restaurant.

This module provides the business logic for deleting an ownership
relationship with validation rules.
"""

from app.domains.restaurants.domain.exceptions import (
    CannotRemovePrimaryOwnerException,
    OwnershipNotFoundException,
)
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class RemoveOwnerUseCase:
    """Use case for removing an owner from a restaurant.

    This use case prevents removing the primary owner if they're the only owner,
    ensuring restaurants always have at least one owner.

    Attributes:
        repository: Restaurant owner repository for data persistence
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
        owner_id: str,
    ) -> bool:
        """Execute the remove owner use case.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner to remove

        Returns:
            True if removed successfully

        Raises:
            OwnershipNotFoundException: If the ownership doesn't exist
            CannotRemovePrimaryOwnerException: If trying to remove the only primary owner
        """
        # Check if ownership exists
        ownership = await self.repository.get_by_ids(restaurant_id, owner_id)
        if not ownership:
            raise OwnershipNotFoundException(restaurant_id, owner_id)

        # If they're primary, check if they're the only owner
        if ownership.is_primary:
            count = await self.repository.count_by_restaurant(restaurant_id)
            if count <= 1:
                raise CannotRemovePrimaryOwnerException(restaurant_id)

        # Remove ownership
        return await self.repository.delete(ownership.id)
