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

    def create(self, favorite_data: FavoriteData) -> Favorite:
        """Create a new favorite.

        Args:
            favorite_data: Data for the new favorite (without ID and timestamp)

        Returns:
            The created favorite entity with generated ID and timestamp

        Raises:
            IntegrityError: If the user has already favorited this entity
        """
        ...

    def delete(self, user_id: str, entity_type: EntityType, entity_id: str) -> bool:
        """Delete a favorite.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

        Returns:
            True if deleted, False if not found
        """
        ...

    def get_by_user(
        self,
        user_id: str,
        entity_type: EntityType | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Favorite], int]:
        """Get favorites for a user with pagination.

        Args:
            user_id: ULID of the user
            entity_type: Optional filter by entity type
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of favorites, total count)
        """
        ...

    def exists(self, user_id: str, entity_type: EntityType, entity_id: str) -> bool:
        """Check if a favorite exists.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

        Returns:
            True if favorite exists, False otherwise
        """
        ...

    def get(
        self, user_id: str, entity_type: EntityType, entity_id: str
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
