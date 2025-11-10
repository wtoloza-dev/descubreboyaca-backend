"""Favorite service implementation.

This module implements the favorite service for business logic orchestration.
"""

from app.domains.favorites.domain.entities import Favorite, FavoriteData
from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.domain.exceptions import FavoriteNotFoundException
from app.domains.favorites.domain.interfaces import FavoriteRepositoryInterface


class FavoriteService:
    """Service for favorite business logic.

    This service orchestrates favorite-related use cases and coordinates
    repository operations. It contains the application's business logic
    for favorites.

    Following the architecture, application services do NOT need abstraction
    (no interface required) as they ARE the business logic.

    Attributes:
        repository: Favorite repository for data access
    """

    def __init__(self, repository: FavoriteRepositoryInterface) -> None:
        """Initialize the service.

        Args:
            repository: Favorite repository implementation
        """
        self.repository = repository

    async def add_favorite(
        self, user_id: str, entity_type: EntityType, entity_id: str
    ) -> Favorite:
        """Add an entity to user's favorites.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity to favorite
            entity_id: ULID of the entity to favorite

        Returns:
            The created favorite

        Raises:
            FavoriteAlreadyExistsException: If already favorited
        """
        favorite_data = FavoriteData(
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return await self.repository.create(favorite_data)

    async def remove_favorite(
        self, user_id: str, entity_type: EntityType, entity_id: str
    ) -> None:
        """Remove an entity from user's favorites.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

        Raises:
            FavoriteNotFoundException: If favorite not found
        """
        deleted = await self.repository.delete(user_id, entity_type, entity_id)
        if not deleted:
            raise FavoriteNotFoundException(
                user_id=user_id,
                entity_type=entity_type.value,
                entity_id=entity_id,
            )

    async def list_favorites(
        self,
        user_id: str,
        entity_type: EntityType | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Favorite], int]:
        """List user's favorites with pagination.

        Args:
            user_id: ULID of the user
            entity_type: Optional filter by entity type
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of favorites, total count)
        """
        return await self.repository.get_by_user(user_id, entity_type, offset, limit)

    async def check_favorite(
        self, user_id: str, entity_type: EntityType, entity_id: str
    ) -> Favorite | None:
        """Check if an entity is favorited by user.

        Args:
            user_id: ULID of the user
            entity_type: Type of entity
            entity_id: ULID of the entity

        Returns:
            The favorite if found, None otherwise
        """
        return await self.repository.get(user_id, entity_type, entity_id)
