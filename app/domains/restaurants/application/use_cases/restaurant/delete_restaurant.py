"""Use case for deleting a restaurant with archiving.

This module provides the business logic for permanently deleting a restaurant
while preserving its data in the archive system using the Unit of Work pattern.
"""

from app.domains.audit.domain import ArchiveData, ArchiveRepositoryInterface
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface
from app.shared.domain.patterns import AsyncUnitOfWork


class DeleteRestaurantUseCase:
    """Use case for deleting a restaurant permanently with archiving.

    This use case implements the Unit of Work pattern to ensure atomicity:
    1. Archives the restaurant record (pending)
    2. Deletes from restaurants table (pending)
    3. Commits both operations atomically (all or nothing)

    **Archiving is mandatory**. The complete restaurant data is preserved
    in the archive table before deletion, maintaining audit trail and
    compliance requirements.

    Attributes:
        restaurant_repository: Restaurant repository for data persistence
        archive_repository: Archive repository for deleted records
    """

    def __init__(
        self,
        restaurant_repository: RestaurantRepositoryInterface,
        archive_repository: ArchiveRepositoryInterface,
    ) -> None:
        """Initialize the use case with dependencies.

        Args:
            restaurant_repository: Restaurant repository implementation
            archive_repository: Archive repository implementation (mandatory)
        """
        self.restaurant_repository = restaurant_repository
        self.archive_repository = archive_repository

    async def execute(
        self,
        restaurant_id: str,
        deleted_by: str | None = None,
        note: str | None = None,
    ) -> None:
        """Execute the delete restaurant use case.

        Args:
            restaurant_id: ULID of the restaurant to delete
            deleted_by: ULID of the user deleting the restaurant
            note: Optional note explaining the deletion reason

        Raises:
            RestaurantNotFoundException: If restaurant is not found

        Example:
            >>> await use_case.execute(
            ...     restaurant_id="01HQZX123456789ABCDEFGHIJK",
            ...     deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0",
            ...     note="Permanently closed",
            ... )
            # Both archive and delete happen atomically
        """
        # Validate restaurant exists
        restaurant = await self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundException(restaurant_id)

        # Prepare archive data
        archive_data = ArchiveData(
            original_table="restaurants",
            original_id=restaurant_id,
            data=restaurant.model_dump(mode="json"),
            note=note,
        )

        # Execute archive and delete atomically using Unit of Work
        async with AsyncUnitOfWork(self.restaurant_repository.session) as uow:
            # Archive WITHOUT committing (managed by UoW)
            await self.archive_repository.create(
                archive_data, deleted_by=deleted_by, commit=False
            )

            # Delete WITHOUT committing (managed by UoW)
            await self.restaurant_repository.delete(
                restaurant_id, deleted_by=deleted_by, commit=False
            )

            # Single atomic commit through UoW
            await uow.commit()
            # If exception occurs, UoW auto-rolls back in __aexit__
