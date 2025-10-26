"""Restaurant owner repository interface.

This module defines the interface contract for RestaurantOwner repository operations
using asynchronous operations.
"""

from typing import Protocol

from app.domains.restaurants.domain.entities import (
    RestaurantOwner,
    RestaurantOwnerData,
)


class RestaurantOwnerRepositoryInterface(Protocol):
    """Interface defining the contract for RestaurantOwner repository.

    This interface defines the operations that can be performed on
    restaurant owner data storage using asynchronous operations.
    """

    async def create(
        self,
        ownership_data: RestaurantOwnerData,
        assigned_by: str | None = None,
        commit: bool = True,
    ) -> RestaurantOwner:
        """Create a new restaurant ownership relationship asynchronously.

        Args:
            ownership_data: Core ownership data
            assigned_by: ULID of the admin who assigned this ownership
            commit: Whether to commit the transaction immediately

        Returns:
            RestaurantOwner: Complete ownership entity with ID and metadata
        """
        ...

    async def get_by_id(self, ownership_id: str) -> RestaurantOwner | None:
        """Get an ownership by its ID asynchronously.

        Args:
            ownership_id: ULID of the ownership

        Returns:
            RestaurantOwner if found, None otherwise
        """
        ...

    async def get_by_ids(
        self, restaurant_id: str, owner_id: str
    ) -> RestaurantOwner | None:
        """Get ownership by restaurant and owner IDs asynchronously.

        Args:
            restaurant_id: ULID of the restaurant
            owner_id: ULID of the owner

        Returns:
            RestaurantOwner if found, None otherwise
        """
        ...

    async def list_by_restaurant(
        self, restaurant_id: str, offset: int = 0, limit: int = 20
    ) -> list[RestaurantOwner]:
        """List all owners of a restaurant asynchronously.

        Args:
            restaurant_id: ULID of the restaurant
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of restaurant owners
        """
        ...

    async def list_by_owner(
        self, owner_id: str, offset: int = 0, limit: int = 20
    ) -> list[RestaurantOwner]:
        """List all restaurants owned by a user asynchronously.

        Args:
            owner_id: ULID of the owner
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of restaurant ownerships for the user
        """
        ...

    async def get_primary_owner(self, restaurant_id: str) -> RestaurantOwner | None:
        """Get the primary owner of a restaurant asynchronously.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Primary RestaurantOwner if found, None otherwise
        """
        ...

    async def is_owner_of_restaurant(self, owner_id: str, restaurant_id: str) -> bool:
        """Check if a user is an owner of a specific restaurant asynchronously.

        Args:
            owner_id: ULID of the user
            restaurant_id: ULID of the restaurant

        Returns:
            True if user is an owner, False otherwise
        """
        ...

    async def get_restaurants_by_owner(self, owner_id: str) -> list[RestaurantOwner]:
        """Get all restaurants owned by a specific user asynchronously.

        Args:
            owner_id: ULID of the owner

        Returns:
            List of restaurant ownerships for the user
        """
        ...

    async def get_owners_by_restaurant(
        self, restaurant_id: str
    ) -> list[RestaurantOwner]:
        """Get all owners of a specific restaurant asynchronously.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            List of owners for the restaurant
        """
        ...

    async def update(
        self,
        ownership_id: str,
        ownership_data: RestaurantOwnerData,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> RestaurantOwner | None:
        """Update an existing ownership relationship asynchronously.

        Args:
            ownership_id: ULID of the ownership to update
            ownership_data: Updated ownership data
            updated_by: ULID of the user who updated the record
            commit: Whether to commit the transaction immediately

        Returns:
            Updated RestaurantOwner if found, None otherwise
        """
        ...

    async def unset_primary_owner(
        self, restaurant_id: str, commit: bool = True
    ) -> bool:
        """Unset the primary owner for a restaurant asynchronously.

        Args:
            restaurant_id: ULID of the restaurant
            commit: Whether to commit the transaction immediately

        Returns:
            True if a primary owner was unset, False if none existed
        """
        ...

    async def delete(self, ownership_id: str, commit: bool = True) -> bool:
        """Delete an ownership relationship asynchronously (hard delete).

        Args:
            ownership_id: ULID of the ownership to delete
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        ...

    async def count_by_restaurant(self, restaurant_id: str) -> int:
        """Count owners for a restaurant asynchronously.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Number of owners for the restaurant
        """
        ...

    async def commit(self) -> None:
        """Commit the current transaction.

        Useful for Unit of Work pattern when commit=False is used in operations.
        """
        ...

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Useful for Unit of Work pattern when an error occurs.
        """
        ...
