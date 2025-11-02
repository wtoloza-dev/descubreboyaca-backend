"""Restaurant business services.

This module provides async services for restaurant business logic.
Services coordinate between repositories and contain domain logic.
"""

from typing import Any

from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.domain.interfaces import FavoriteRepositoryInterface
from app.domains.restaurants.domain import (
    Restaurant,
    RestaurantData,
)
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface
from app.domains.audit.domain import AsyncArchiveRepositoryInterface
from app.shared.domain.patterns import AsyncUnitOfWork


class RestaurantService:
    """Restaurant service for managing restaurant operations.

    This service provides business logic for restaurant operations including
    CRUD operations and archiving deleted restaurants using async operations.

    The service follows the principle of depending only on repositories (one level below).
    It obtains the database session from the repository when needed for Unit of Work,
    maintaining clean architecture boundaries.

    Attributes:
        repository: Restaurant repository for data persistence
        archive_repository: Archive repository for deleted records
        favorite_repository: Favorite repository for user favorites (optional)
    """

    def __init__(
        self,
        repository: RestaurantRepositoryInterface,
        archive_repository: AsyncArchiveRepositoryInterface,
        favorite_repository: FavoriteRepositoryInterface | None = None,
    ) -> None:
        """Initialize restaurant service.

        The service depends only on repository interfaces, not on infrastructure
        details like database sessions. This maintains proper separation of concerns.

        Args:
            repository: Restaurant repository implementation
            archive_repository: Archive repository implementation (mandatory)
            favorite_repository: Favorite repository implementation (optional, needed for favorite operations)
        """
        self.repository = repository
        self.archive_repository = archive_repository
        self.favorite_repository = favorite_repository

    async def create_restaurant(
        self, restaurant_data: RestaurantData, created_by: str | None = None
    ) -> Restaurant:
        """Create a new restaurant.

        Args:
            restaurant_data: Restaurant data without system metadata
            created_by: ULID of the user creating the restaurant

        Returns:
            Restaurant: Created restaurant with ID and metadata
        """
        return await self.repository.create(restaurant_data, created_by=created_by)

    async def get_restaurant_by_id(self, restaurant_id: str) -> Restaurant:
        """Get a restaurant by its ID.

        Args:
            restaurant_id: ULID of the restaurant

        Returns:
            Restaurant: The found restaurant

        Raises:
            RestaurantNotFoundException: If restaurant is not found
        """
        restaurant = await self.repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)
        return restaurant

    async def find_restaurants(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Restaurant]:
        """Find restaurants with dynamic filters and pagination.

        Args:
            filters: Dictionary of field names and their values to filter by
            offset: Number of records to offset
            limit: Maximum number of records to return

        Returns:
            List of restaurants matching the filters

        Example:
            >>> restaurants = await service.find_restaurants()
            >>> restaurants = await service.find_restaurants({"city": "Tunja"})
            >>> restaurants = await service.find_restaurants(
            ...     {"city": "Tunja", "price_level": 2}, offset=0, limit=10
            ... )
        """
        return await self.repository.find(filters=filters, offset=offset, limit=limit)

    async def count_restaurants(self, filters: dict[str, Any] | None = None) -> int:
        """Count restaurants with dynamic filters.

        Args:
            filters: Dictionary of field names and their values to filter by

        Returns:
            Count of restaurants matching the filters

        Example:
            >>> total = await service.count_restaurants()
            >>> total = await service.count_restaurants({"city": "Tunja"})
            >>> total = await service.count_restaurants(
            ...     {"city": "Tunja", "price_level": 2}
            ... )
        """
        return await self.repository.count(filters=filters)

    async def list_restaurants(
        self, offset: int = 0, limit: int = 20
    ) -> list[Restaurant]:
        """List all restaurants with pagination.

        Args:
            offset: Number of records to offset
            limit: Maximum number of records to return

        Returns:
            List of restaurants
        """
        return await self.find_restaurants(offset=offset, limit=limit)

    async def list_restaurants_by_city(
        self, city: str, offset: int = 0, limit: int = 20
    ) -> list[Restaurant]:
        """List restaurants by city.

        Args:
            city: City name to filter by
            offset: Number of records to offset
            limit: Maximum number of records to return

        Returns:
            List of restaurants in the specified city
        """
        return await self.find_restaurants(
            filters={"city": city}, offset=offset, limit=limit
        )

    async def count_all_restaurants(self) -> int:
        """Count total number of restaurants.

        Returns:
            Total count of restaurants
        """
        return await self.count_restaurants()

    async def count_restaurants_by_city(self, city: str) -> int:
        """Count restaurants by city.

        Args:
            city: City name to filter by

        Returns:
            Count of restaurants in the specified city
        """
        return await self.count_restaurants(filters={"city": city})

    async def update_restaurant(
        self,
        restaurant_id: str,
        restaurant_data: RestaurantData,
        updated_by: str | None = None,
    ) -> Restaurant:
        """Update an existing restaurant.

        Args:
            restaurant_id: ULID of the restaurant to update
            restaurant_data: Updated restaurant data
            updated_by: ULID of the user updating the restaurant

        Returns:
            Restaurant: Updated restaurant

        Raises:
            RestaurantNotFoundException: If restaurant is not found
        """
        updated = await self.repository.update(
            restaurant_id, restaurant_data, updated_by=updated_by
        )
        if not updated:
            raise RestaurantNotFoundException(restaurant_id)
        return updated

    async def deactivate_restaurant(
        self, restaurant_id: str, updated_by: str | None = None
    ) -> None:
        """Deactivate a restaurant (soft delete).

        Args:
            restaurant_id: ULID of the restaurant to deactivate
            updated_by: ULID of the user deactivating the restaurant

        Raises:
            RestaurantNotFoundException: If restaurant is not found
        """
        success = await self.repository.deactivate(restaurant_id, updated_by=updated_by)
        if not success:
            raise RestaurantNotFoundException(restaurant_id)

    async def delete_restaurant(
        self,
        restaurant_id: str,
        deleted_by: str | None = None,
        note: str | None = None,
    ) -> None:
        """Delete a restaurant permanently with archiving using Unit of Work.

        This method implements the Unit of Work pattern to ensure atomicity:
        1. Archives the restaurant record (pending)
        2. Deletes from restaurants table (pending)
        3. Commits both operations atomically (all or nothing)

        **Archiving is mandatory**. The complete restaurant data is preserved
        in the archive table before deletion, maintaining audit trail and
        compliance requirements.

        **Unit of Work guarantees**:
        - Atomicity: Both archive and delete succeed together or fail together
        - Consistency: No partial deletions (archive without delete or vice versa)
        - Isolation: Operations happen in single database transaction
        - Durability: Changes persist only on successful commit

        Args:
            restaurant_id: ULID of the restaurant to delete
            deleted_by: ULID of the user deleting the restaurant
            note: Optional note explaining the deletion reason

        Raises:
            RestaurantNotFoundException: If restaurant is not found

        Example:
            >>> await service.delete_restaurant(
            ...     restaurant_id="01HQZX123456789ABCDEFGHIJK",
            ...     deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0",
            ...     note="Permanently closed",
            ... )
            # Both archive and delete happen atomically
        """
        # Validate restaurant exists
        restaurant = await self.repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)

        # Prepare archive data
        from app.domains.audit.domain import ArchiveData

        archive_data = ArchiveData(
            original_table="restaurants",
            original_id=restaurant_id,
            data=restaurant.model_dump(mode="json"),
            note=note,
        )

        # Execute archive and delete atomically using Unit of Work
        # Get session from repository (clean architecture: service → repository → session)
        async with AsyncUnitOfWork(self.repository.session) as uow:
            # Archive WITHOUT committing (managed by UoW)
            await self.archive_repository.create(
                archive_data, deleted_by=deleted_by, commit=False
            )

            # Delete WITHOUT committing (managed by UoW)
            await self.repository.delete(restaurant_id, commit=False)

            # Single atomic commit through UoW
            await uow.commit()
            # If exception occurs, UoW auto-rolls back in __aexit__

    async def list_user_favorites(
        self,
        user_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Restaurant], int]:
        """List restaurants favorited by a user with pagination.

        This method retrieves all restaurants that a user has marked as favorites.
        It uses the favorite repository to get the list of favorite entity IDs,
        then fetches the complete restaurant data for each one.

        Args:
            user_id: ULID of the user
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of favorite restaurants, total count)

        Raises:
            ValueError: If favorite_repository is not available

        Example:
            >>> restaurants, total = await service.list_user_favorites(
            ...     user_id="01BX5ZZKBKACTAV9WEVGEMMVS0",
            ...     offset=0,
            ...     limit=10,
            ... )
        """
        if not self.favorite_repository:
            raise ValueError(
                "Favorite repository is required for this operation. "
                "Please provide it when initializing the service."
            )

        # Get user's favorite restaurants
        favorites, total = await self.favorite_repository.get_by_user(
            user_id=user_id,
            entity_type=EntityType.RESTAURANT,
            offset=offset,
            limit=limit,
        )

        # Extract restaurant IDs from favorites
        restaurant_ids = [favorite.entity_id for favorite in favorites]

        # If no favorites, return empty list
        if not restaurant_ids:
            return [], 0

        # Fetch complete restaurant data for each favorite
        # Note: This could be optimized with a bulk query in the repository
        restaurants = []
        for restaurant_id in restaurant_ids:
            restaurant = await self.repository.get_by_id(restaurant_id)
            if restaurant:  # Only add if restaurant still exists
                restaurants.append(restaurant)

        return restaurants, total
