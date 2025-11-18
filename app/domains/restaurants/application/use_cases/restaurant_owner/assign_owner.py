"""Use case for assigning an owner to a restaurant.

This module provides the business logic for creating an ownership
relationship between a user and a restaurant.
"""

from app.domains.restaurants.domain.entities import (
    RestaurantOwner,
    RestaurantOwnerData,
)
from app.domains.restaurants.domain.exceptions import OwnershipAlreadyExistsException
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class AssignOwnerUseCase:
    """Use case for assigning an owner to a restaurant.

    This use case creates a new ownership relationship and handles
    primary ownership assignment by unsetting existing primary owners.

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
        role: str = "owner",
        is_primary: bool = False,
        assigned_by: str | None = None,
    ) -> RestaurantOwner:
        """Execute the assign owner use case.

        If is_primary is True, this will automatically unset any existing
        primary owner for the restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the user to assign as owner
            role: Role of the owner (owner, manager, staff)
            is_primary: Whether this is the primary owner
            assigned_by: ULID of the admin who assigned this ownership

        Returns:
            RestaurantOwner: The created ownership relationship

        Raises:
            OwnershipAlreadyExistsException: If the relationship already exists
        """
        # Check if relationship already exists
        existing = await self.repository.get_by_ids(restaurant_id, owner_id)
        if existing:
            raise OwnershipAlreadyExistsException(restaurant_id, owner_id)

        # Create owner data
        owner_data = RestaurantOwnerData(
            restaurant_id=restaurant_id,
            owner_id=owner_id,
            role=role,
            is_primary=is_primary,
        )

        # If this is primary, unset existing primary
        if is_primary:
            await self.repository.unset_primary_owner(restaurant_id, commit=False)

        # Assign owner
        result = await self.repository.create(
            ownership_data=owner_data, assigned_by=assigned_by, commit=True
        )
        return result
