"""Use case for updating an owner's role.

This module provides the business logic for changing an owner's role
within a restaurant.
"""

from app.domains.restaurants.domain.entities import (
    RestaurantOwner,
    RestaurantOwnerData,
)
from app.domains.restaurants.domain.exceptions import (
    InvalidOwnerRoleException,
    OwnershipNotFoundException,
)
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class UpdateOwnerRoleUseCase:
    """Use case for updating an owner's role.

    This use case validates the new role and updates the ownership relationship
    while maintaining other attributes.

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
        new_role: str,
        updated_by: str | None = None,
    ) -> RestaurantOwner:
        """Execute the update owner role use case.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner
            new_role: New role to assign
            updated_by: ULID of the admin who updated the role

        Returns:
            RestaurantOwner: Updated ownership relationship

        Raises:
            OwnershipNotFoundException: If the ownership doesn't exist
            InvalidOwnerRoleException: If the new role is invalid
        """
        # Validate role
        valid_roles = ["owner", "manager", "staff"]
        if new_role not in valid_roles:
            raise InvalidOwnerRoleException(new_role)

        # Get existing ownership
        ownership = await self.repository.get_by_ids(restaurant_id, owner_id)
        if not ownership:
            raise OwnershipNotFoundException(restaurant_id, owner_id)

        # Update owner data
        updated_data = RestaurantOwnerData(
            restaurant_id=ownership.restaurant_id,
            owner_id=ownership.owner_id,
            role=new_role,
            is_primary=ownership.is_primary,
        )

        result = await self.repository.update(
            ownership_id=ownership.id,
            ownership_data=updated_data,
            updated_by=updated_by,
        )

        if not result:
            raise OwnershipNotFoundException(restaurant_id, owner_id)

        return result
