"""Restaurant owner business services.

This module provides async services for restaurant ownership business logic.
Services coordinate between repositories and contain domain logic for
managing restaurant ownership relationships.
"""

from app.domains.restaurants.domain.entities import (
    RestaurantOwner,
    RestaurantOwnerData,
)
from app.domains.restaurants.domain.exceptions import (
    CannotRemovePrimaryOwnerException,
    InvalidOwnerRoleException,
    OwnerNotAssignedException,
    OwnershipAlreadyExistsException,
    OwnershipNotFoundException,
)
from app.domains.restaurants.domain.interfaces import (
    RestaurantOwnerRepositoryInterface,
)


class RestaurantOwnerService:
    """Restaurant owner service for managing ownership operations.

    This service provides business logic for restaurant ownership operations
    including assigning/removing owners, managing roles, and transferring ownership.

    Attributes:
        repository: Restaurant owner repository for data persistence
    """

    def __init__(
        self,
        repository: RestaurantOwnerRepositoryInterface,
    ) -> None:
        """Initialize restaurant owner service.

        Args:
            repository: Restaurant owner repository implementation
        """
        self.repository = repository

    async def assign_owner(
        self,
        restaurant_id: str,
        owner_id: str,
        role: str = "owner",
        is_primary: bool = False,
        assigned_by: str | None = None,
    ) -> RestaurantOwner:
        """Assign an owner to a restaurant.

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

    async def remove_owner(
        self,
        restaurant_id: str,
        owner_id: str,
    ) -> bool:
        """Remove an owner from a restaurant.

        Prevents removing the primary owner if they're the only owner.

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

    async def update_owner_role(
        self,
        restaurant_id: str,
        owner_id: str,
        new_role: str,
        updated_by: str | None = None,
    ) -> RestaurantOwner:
        """Update an owner's role.

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

    async def transfer_primary_ownership(
        self,
        restaurant_id: str,
        new_owner_id: str,
        transferred_by: str | None = None,
    ) -> RestaurantOwner:
        """Transfer primary ownership to another owner.

        The new owner must already be an owner of the restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            new_owner_id: ULID of the user to make primary owner
            transferred_by: ULID of the admin who transferred ownership

        Returns:
            RestaurantOwner: Updated ownership relationship for the new primary owner

        Raises:
            OwnerNotAssignedException: If the new owner is not already an owner
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

    async def list_restaurant_owners(
        self,
        restaurant_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[RestaurantOwner]:
        """List all owners of a restaurant.

        Args:
            restaurant_id: ULID of the restaurant
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of restaurant owners
        """
        return await self.repository.list_by_restaurant(restaurant_id, offset, limit)

    async def list_user_restaurants(
        self,
        owner_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> list[RestaurantOwner]:
        """List all restaurants owned by a user.

        Args:
            owner_id: ULID of the owner
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of restaurant ownerships for the user
        """
        return await self.repository.list_by_owner(owner_id, offset, limit)

    async def get_primary_owner(self, restaurant_id: str) -> RestaurantOwner | None:
        """Get the primary owner of a restaurant.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Primary RestaurantOwner if found, None otherwise
        """
        return await self.repository.get_primary_owner(restaurant_id)

    async def verify_ownership(
        self, owner_id: str, restaurant_id: str
    ) -> RestaurantOwner | None:
        """Verify that a user is an owner of a specific restaurant.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Returns:
            RestaurantOwner if user is an owner, None otherwise
        """
        return await self.repository.get_by_ids(restaurant_id, owner_id)

    async def is_owner_of_restaurant(self, owner_id: str, restaurant_id: str) -> bool:
        """Check if a user is an owner of a specific restaurant.

        This is a convenience method that returns a boolean instead of
        the ownership relationship entity.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Returns:
            True if user is an owner, False otherwise
        """
        return await self.repository.is_owner_of_restaurant(owner_id, restaurant_id)

    async def require_ownership(self, owner_id: str, restaurant_id: str) -> None:
        """Verify that a user owns a restaurant, raise exception if not.

        This method encapsulates the ownership verification logic,
        preventing routes from directly handling domain exceptions.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Raises:
            InsufficientPermissionsException: If user is not an owner of the restaurant
        """
        from app.domains.auth.domain.exceptions import InsufficientPermissionsException

        is_owner = await self.is_owner_of_restaurant(owner_id, restaurant_id)
        if not is_owner:
            raise InsufficientPermissionsException(
                f"User {owner_id} does not have permission to access restaurant {restaurant_id}"
            )

    async def get_restaurants_by_owner(self, owner_id: str) -> list[RestaurantOwner]:
        """Get all restaurants owned by a specific user.

        This method retrieves all restaurant ownership relationships
        for a given user, useful for listing "My Restaurants".

        Args:
            owner_id: ULID of the owner

        Returns:
            List of restaurant ownerships for the user
        """
        return await self.repository.get_restaurants_by_owner(owner_id)

    async def get_owners_by_restaurant(
        self, restaurant_id: str
    ) -> list[RestaurantOwner]:
        """Get all owners/team members of a specific restaurant.

        This method retrieves all ownership relationships for a restaurant,
        useful for listing team members.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            List of owners/team members for the restaurant
        """
        return await self.repository.get_owners_by_restaurant(restaurant_id)
