"""Restaurant repository interface.

This module defines the interface contract for Restaurant repository operations
using asynchronous operations.
"""

from typing import Any, Protocol

from app.domains.restaurants.domain import Restaurant, RestaurantData


class RestaurantRepositoryInterface(Protocol):
    """Interface defining the contract for Restaurant repository.

    This interface defines the operations that can be performed on
    restaurant data storage using asynchronous operations.
    """

    async def create(
        self,
        restaurant_data: RestaurantData,
        created_by: str | None = None,
        commit: bool = True,
    ) -> Restaurant:
        """Create a new restaurant asynchronously.

        Args:
            restaurant_data: Core restaurant data without system metadata
            created_by: ULID of the user who created the record
            commit: Whether to commit the transaction immediately

        Returns:
            Restaurant: Complete restaurant entity with ID and system metadata
        """
        ...

    async def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        """Get a restaurant by its ID asynchronously.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Restaurant if found, None otherwise
        """
        ...

    async def find(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Restaurant]:
        """Find restaurants with dynamic filters and pagination asynchronously.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match model attribute names.
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            List of restaurants matching the filters
        """
        ...

    async def update(
        self,
        restaurant_id: str,
        restaurant_data: RestaurantData,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> Restaurant | None:
        """Update an existing restaurant asynchronously.

        Args:
            restaurant_id: ULID of the restaurant to update
            restaurant_data: Updated restaurant data
            updated_by: ULID of the user who updated the record
            commit: Whether to commit the transaction immediately

        Returns:
            Updated Restaurant if found, None otherwise
        """
        ...

    async def delete(
        self,
        restaurant_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete a restaurant asynchronously (hard delete).

        Args:
            restaurant_id: ULID of the restaurant to delete
            deleted_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        ...

    async def deactivate(
        self, restaurant_id: str, updated_by: str | None = None
    ) -> bool:
        """Deactivate a restaurant asynchronously (soft delete).

        Args:
            restaurant_id: ULID of the restaurant to deactivate
            updated_by: ULID of the user who deactivated the record

        Returns:
            True if deactivated, False if not found
        """
        ...

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count restaurants with dynamic filters asynchronously.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match model attribute names.

        Returns:
            Count of restaurants matching the filters
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
