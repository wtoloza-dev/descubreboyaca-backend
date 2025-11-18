"""Use case for transferring primary ownership.

This module provides the business logic for transferring primary ownership
from one owner to another within a restaurant.
"""

from app.domains.restaurants.domain.entities import (
    RestaurantOwner,
    RestaurantOwnerData,
)
from app.domains.restaurants.domain.exceptions import (
    OwnerNotAssignedException,
    OwnershipNotFoundException,
)
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class TransferPrimaryOwnershipUseCase:
    """Use case for transferring primary ownership to another owner.

    This use case ensures the new owner is already assigned to the restaurant
    before transferring primary ownership.

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
        new_owner_id: str,
        transferred_by: str | None = None,
    ) -> RestaurantOwner:
        """Execute the transfer primary ownership use case.

        The new owner must already be an owner of the restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            new_owner_id: ULID of the user to make primary owner
            transferred_by: ULID of the admin who transferred ownership

        Returns:
            RestaurantOwner: Updated ownership relationship for the new primary owner

        Raises:
            OwnerNotAssignedException: If the new owner is not already an owner
            OwnershipNotFoundException: If update fails
        """
        # Check if new owner is already an owner
        new_owner_ownership = await self.repository.get_by_ids(
            restaurant_id, new_owner_id
        )
        if not new_owner_ownership:
            raise OwnerNotAssignedException(restaurant_id, new_owner_id)

        # Unset current primary
        await self.repository.unset_primary_owner(restaurant_id, commit=False)

        # Update new owner to primary
        updated_data = RestaurantOwnerData(
            restaurant_id=new_owner_ownership.restaurant_id,
            owner_id=new_owner_ownership.owner_id,
            role=new_owner_ownership.role,
            is_primary=True,
        )

        result = await self.repository.update(
            ownership_id=new_owner_ownership.id,
            ownership_data=updated_data,
            updated_by=transferred_by,
            commit=True,
        )

        if not result:
            raise OwnershipNotFoundException(restaurant_id, new_owner_id)

        return result
