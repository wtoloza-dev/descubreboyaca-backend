"""Favorite repository interface.

This module defines the contract for favorite repository implementations.
"""

from typing import Protocol

from app.domains.favorites.domain.entities import Favorite, FavoriteData
from app.domains.favorites.domain.enums import EntityType


class FavoriteRepositoryInterface(Protocol):
    """Interface for favorite repository operations.

    This interface defines the contract that all favorite repository
    implementations must fulfill. It follows the Dependency Inversion
    Principle, allowing services to depend on abstractions rather than
    concrete implementations.
    """

    async def create(
        self,
        favorite_data: FavoriteData,
        created_by: str,
        commit: bool = True,
    ) -> Favorite:
        """Create a new favorite.

        Args:
            favorite_data: Data for the new favorite (without ID and timestamp)
            created_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            The created favorite entity with generated ID and timestamp

        Raises:
            IntegrityError: If the user has already favorited this entity
        """
        ...

    async def delete(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete a favorite (soft delete).

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity
            deleted_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        ...

    async def find(
        self,
        user_id: str,
        entity_type: EntityType | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Favorite]:
        """Find favorites with filters and pagination.

        Args:
            user_id: ULID of the user
            entity_type: Optional filter by entity type
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of favorites matching the filters
        """
        ...

    async def count(
        self,
        user_id: str,
        entity_type: EntityType | None = None,
    ) -> int:
        """Count favorites with filters.

        Args:
            user_id: ULID of the user
            entity_type: Optional filter by entity type

        Returns:
            Count of favorites matching the filters
        """
        ...

    async def find_with_count(
        self,
        user_id: str,
        entity_type: EntityType | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Favorite], int]:
        """Find favorites with filters and pagination, including total count.

        This method returns both the paginated results and the total count
        in a single operation, ensuring consistency between the two queries.

        Args:
            user_id: ULID of the user
            entity_type: Optional filter by entity type
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of favorites, total count)
        """
        ...

    async def get_by_user(
        self,
        user_id: str,
        entity_type: EntityType | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Favorite], int]:
        """Get favorites for a user with pagination.

        Deprecated: Use find_with_count() instead for consistency.

        Args:
            user_id: ULID of the user
            entity_type: Optional filter by entity type
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of favorites, total count)
        """
        ...

    async def exists(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
    ) -> bool:
        """Check if a favorite exists.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

        Returns:
            True if favorite exists, False otherwise
        """
        ...

    async def get(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
    ) -> Favorite | None:
        """Get a specific favorite.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

        Returns:
            The favorite if found, None otherwise
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
