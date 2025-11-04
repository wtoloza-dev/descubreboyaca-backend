"""Dish business services.

This module provides async services for dish business logic.
Services coordinate between repositories and contain domain logic.
"""

from typing import Any

from app.domains.audit.domain import ArchiveRepositoryInterface
from app.domains.restaurants.domain import Dish, DishData
from app.domains.restaurants.domain.exceptions import (
    DishNotFoundException,
    RestaurantNotFoundException,
)
from app.domains.restaurants.domain.interfaces import (
    DishRepositoryInterface,
    RestaurantRepositoryInterface,
)
from app.shared.domain.patterns import AsyncUnitOfWork


class DishService:
    """Dish service for managing dish operations.

    This service provides business logic for dish operations including
    CRUD operations with validation of restaurant existence and ownership.

    The service depends on DishRepository, RestaurantRepository, and
    ArchiveRepository to ensure referential integrity and archiving.

    Attributes:
        dish_repository: Dish repository for data persistence
        restaurant_repository: Restaurant repository for validation
        archive_repository: Archive repository for deleted records
    """

    def __init__(
        self,
        dish_repository: DishRepositoryInterface,
        restaurant_repository: RestaurantRepositoryInterface,
        archive_repository: ArchiveRepositoryInterface,
    ) -> None:
        """Initialize dish service.

        Args:
            dish_repository: Dish repository implementation
            restaurant_repository: Restaurant repository for validation
            archive_repository: Archive repository implementation (mandatory)
        """
        self.dish_repository = dish_repository
        self.restaurant_repository = restaurant_repository
        self.archive_repository = archive_repository

    async def create_dish(
        self,
        dish_data: DishData,
        restaurant_id: str,
        created_by: str | None = None,
    ) -> Dish:
        """Create a new dish for a restaurant.

        Args:
            dish_data: Dish data without system metadata
            restaurant_id: ULID of the restaurant this dish belongs to
            created_by: ULID of the user creating the dish

        Returns:
            Dish: Created dish with ID and metadata

        Raises:
            RestaurantNotFoundException: If the restaurant doesn't exist
        """
        # Validate restaurant exists
        restaurant = await self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)

        # Create dish
        return await self.dish_repository.create(
            dish_data, restaurant_id=restaurant_id, created_by=created_by
        )

    async def get_dish_by_id(self, dish_id: str) -> Dish:
        """Get a dish by its ID.

        Args:
            dish_id: ULID of the dish

        Returns:
            Dish: The found dish

        Raises:
            DishNotFoundException: If dish is not found
        """
        dish = await self.dish_repository.get_by_id(dish_id)
        if not dish:
            raise DishNotFoundException(dish_id)
        return dish

    async def get_restaurant_dishes(
        self,
        restaurant_id: str,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Dish], int]:
        """Get all dishes for a specific restaurant with pagination.

        Args:
            restaurant_id: ULID of the restaurant
            filters: Optional filters (category, is_available, is_featured)
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of dishes, total count)

        Raises:
            RestaurantNotFoundException: If the restaurant doesn't exist
        """
        # Validate restaurant exists
        restaurant = await self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)

        # Get dishes
        dishes = await self.dish_repository.get_by_restaurant_id(
            restaurant_id, filters=filters, offset=offset, limit=limit
        )

        # Get total count
        total_count = await self.dish_repository.count_by_restaurant_id(
            restaurant_id, filters=filters
        )

        return dishes, total_count

    async def update_dish(
        self,
        dish_id: str,
        dish_data: DishData,
        updated_by: str | None = None,
    ) -> Dish:
        """Update an existing dish.

        Args:
            dish_id: ULID of the dish to update
            dish_data: Updated dish data
            updated_by: ULID of the user updating the dish

        Returns:
            Dish: Updated dish

        Raises:
            DishNotFoundException: If dish is not found
        """
        # Verify dish exists
        await self.get_dish_by_id(dish_id)

        updated = await self.dish_repository.update(
            dish_id, dish_data, updated_by=updated_by
        )

        if not updated:
            raise DishNotFoundException(dish_id)

        return updated

    async def delete_dish(
        self,
        dish_id: str,
        deleted_by: str | None = None,
        note: str | None = None,
    ) -> None:
        """Delete a dish permanently with archiving using Unit of Work.

        This method implements the Unit of Work pattern to ensure atomicity:
        1. Archives the dish record (pending)
        2. Deletes from dishes table (pending)
        3. Commits both operations atomically (all or nothing)

        **Archiving is mandatory**. The complete dish data is preserved
        in the archive table before deletion, maintaining audit trail.

        **Unit of Work guarantees**:
        - Atomicity: Both archive and delete succeed together or fail together
        - Consistency: No partial deletions (archive without delete or vice versa)
        - Isolation: Operations happen in single database transaction
        - Durability: Changes persist only on successful commit

        Args:
            dish_id: ULID of the dish to delete
            deleted_by: ULID of the user deleting the dish
            note: Optional note explaining the deletion reason

        Raises:
            DishNotFoundException: If dish is not found

        Example:
            >>> await service.delete_dish(
            ...     dish_id="01HQZX123456789ABCDEFGHIJK",
            ...     deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0",
            ...     note="Discontinued item",
            ... )
            # Both archive and delete happen atomically
        """
        # Validate dish exists
        dish = await self.dish_repository.get_by_id(dish_id)
        if not dish:
            raise DishNotFoundException(dish_id)

        # Prepare archive data
        from app.domains.audit.domain import ArchiveData

        archive_data = ArchiveData(
            original_table="dishes",
            original_id=dish_id,
            data=dish.model_dump(mode="json"),
            note=note,
        )

        # Execute archive and delete atomically using Unit of Work
        # Get session from repository (clean architecture: service → repository → session)
        async with AsyncUnitOfWork(self.dish_repository.session) as uow:
            # Archive WITHOUT committing (managed by UoW)
            await self.archive_repository.create(
                archive_data, deleted_by=deleted_by, commit=False
            )

            # Delete WITHOUT committing (managed by UoW)
            await self.dish_repository.delete(dish_id, commit=False)

            # Single atomic commit through UoW
            await uow.commit()
            # If exception occurs, UoW auto-rolls back in __aexit__

    async def toggle_availability(
        self,
        dish_id: str,
        is_available: bool,
        updated_by: str | None = None,
    ) -> Dish:
        """Toggle dish availability (soft enable/disable).

        Args:
            dish_id: ULID of the dish
            is_available: New availability status
            updated_by: ULID of the user making the change

        Returns:
            Dish: Updated dish

        Raises:
            DishNotFoundException: If dish is not found
        """
        # Get current dish (raises exception if not found)
        dish = await self.get_dish_by_id(dish_id)

        # Update only is_available field
        dish_data = DishData(
            name=dish.name,
            description=dish.description,
            category=dish.category,
            price=dish.price,
            original_price=dish.original_price,
            is_available=is_available,  # Toggle this
            preparation_time_minutes=dish.preparation_time_minutes,
            serves=dish.serves,
            calories=dish.calories,
            image_url=dish.image_url,
            dietary_restrictions=dish.dietary_restrictions,
            ingredients=dish.ingredients,
            allergens=dish.allergens,
            flavor_profile=dish.flavor_profile,
            is_featured=dish.is_featured,
            display_order=dish.display_order,
        )

        updated = await self.dish_repository.update(
            dish_id, dish_data, updated_by=updated_by
        )

        if not updated:
            raise DishNotFoundException(dish_id)

        return updated

    async def list_dishes(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Dish], int]:
        """List all dishes with optional filters and pagination.

        Args:
            filters: Optional filters (restaurant_id, category, is_available, etc.)
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of dishes, total count)
        """
        dishes = await self.dish_repository.find(
            filters=filters, offset=offset, limit=limit
        )

        total_count = await self.dish_repository.count(filters=filters)

        return dishes, total_count
