"""Dish repository interface.

This module defines the interface contract for Dish repository operations
using asynchronous operations.
"""

from typing import Any, Protocol

from app.domains.restaurants.domain.entities import Dish, DishData


class DishRepositoryInterface(Protocol):
    """Interface defining the contract for Dish repository.

    This interface defines the operations that can be performed on
    dish data storage using asynchronous operations.
    """

    async def create(
        self,
        dish_data: DishData,
        restaurant_id: str,
        created_by: str | None = None,
        commit: bool = True,
    ) -> Dish:
        """Create a new dish asynchronously.

        Args:
            dish_data: Core dish data without system metadata
            restaurant_id: ULID of the restaurant this dish belongs to
            created_by: ULID of the user who created the record
            commit: Whether to commit the transaction immediately

        Returns:
            Dish: Complete dish entity with ID and system metadata
        """
        ...

    async def get_by_id(self, dish_id: str) -> Dish | None:
        """Get a dish by its ID asynchronously.

        Args:
            dish_id: ULID of the dish

        Returns:
            Dish if found, None otherwise
        """
        ...

    async def get_by_restaurant_id(
        self,
        restaurant_id: str,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Dish]:
        """Get all dishes for a specific restaurant asynchronously.

        Args:
            restaurant_id: ULID of the restaurant
            filters: Optional additional filters (category, is_available, etc.)
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            List of dishes belonging to the restaurant
        """
        ...

    async def find(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Dish]:
        """Find dishes with dynamic filters and pagination asynchronously.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match model attribute names.
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            List of dishes matching the filters
        """
        ...

    async def update(
        self,
        dish_id: str,
        dish_data: DishData,
        updated_by: str | None = None,
        commit: bool = True,
    ) -> Dish | None:
        """Update an existing dish asynchronously.

        Args:
            dish_id: ULID of the dish to update
            dish_data: Updated dish data
            updated_by: ULID of the user who updated the record
            commit: Whether to commit the transaction immediately

        Returns:
            Updated Dish if found, None otherwise
        """
        ...

    async def delete(
        self,
        dish_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete a dish asynchronously (soft delete).

        Args:
            dish_id: ULID of the dish to delete
            deleted_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        ...

    async def count(
        self,
        filters: dict[str, Any] | None = None,
    ) -> int:
        """Count dishes with dynamic filters asynchronously.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match model attribute names.

        Returns:
            Count of dishes matching the filters
        """
        ...

    async def count_by_restaurant_id(
        self,
        restaurant_id: str,
        filters: dict[str, Any] | None = None,
    ) -> int:
        """Count dishes for a specific restaurant asynchronously.

        Args:
            restaurant_id: ULID of the restaurant
            filters: Optional additional filters (category, is_available, etc.)

        Returns:
            Count of dishes belonging to the restaurant
        """
        ...

    async def find_with_count(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Dish], int]:
        """Find dishes with filters and pagination, including total count.

        This method returns both the paginated results and the total count
        in a single operation, ensuring consistency between the two queries.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match model attribute names.
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of dishes, total count)
        """
        ...

    async def find_with_count_by_restaurant_id(
        self,
        restaurant_id: str,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Dish], int]:
        """Find dishes for a restaurant with pagination, including total count.

        This method returns both the paginated results and the total count
        in a single operation, ensuring consistency between the two queries.

        Args:
            restaurant_id: ULID of the restaurant
            filters: Optional additional filters (category, is_available, etc.)
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of dishes, total count)
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
