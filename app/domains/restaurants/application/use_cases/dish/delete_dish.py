"""Use case for deleting a dish with archiving.

This module provides the business logic for permanently deleting a dish
while preserving its data in the archive system using the Unit of Work pattern.
"""

from app.domains.audit.domain import ArchiveData, ArchiveRepositoryInterface
from app.domains.restaurants.domain.exceptions import DishNotFoundException
from app.domains.restaurants.domain.interfaces import DishRepositoryInterface
from app.shared.domain.patterns import AsyncUnitOfWork


class DeleteDishUseCase:
    """Use case for deleting a dish permanently with archiving.

    This use case implements the Unit of Work pattern to ensure atomicity:
    1. Archives the dish record (pending)
    2. Deletes from dishes table (pending)
    3. Commits both operations atomically (all or nothing)

    **Archiving is mandatory**. The complete dish data is preserved
    in the archive table before deletion, maintaining audit trail.

    Attributes:
        dish_repository: Dish repository for data persistence
        archive_repository: Archive repository for deleted records
    """

    def __init__(
        self,
        dish_repository: DishRepositoryInterface,
        archive_repository: ArchiveRepositoryInterface,
    ) -> None:
        """Initialize the use case with dependencies.

        Args:
            dish_repository: Dish repository implementation
            archive_repository: Archive repository implementation (mandatory)
        """
        self.dish_repository = dish_repository
        self.archive_repository = archive_repository

    async def execute(
        self,
        dish_id: str,
        deleted_by: str | None = None,
        note: str | None = None,
    ) -> None:
        """Execute the delete dish use case.

        Args:
            dish_id: ULID of the dish to delete
            deleted_by: ULID of the user deleting the dish
            note: Optional note explaining the deletion reason

        Raises:
            DishNotFoundException: If dish is not found

        Example:
            >>> await use_case.execute(
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
        archive_data = ArchiveData(
            original_table="dishes",
            original_id=dish_id,
            data=dish.model_dump(mode="json"),
            note=note,
        )

        # Execute archive and delete atomically using Unit of Work
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
