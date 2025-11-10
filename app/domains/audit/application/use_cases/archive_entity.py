"""Archive entity use case.

This module contains the use case for archiving an entity when it's deleted
from the system.
"""

from typing import Any

from pydantic import BaseModel

from app.domains.audit.domain import (
    Archive,
    ArchiveData,
    ArchiveRepositoryInterface,
)


class ArchiveEntityUseCase:
    """Use case for archiving a deleted entity.

    This use case handles the complete workflow of archiving an entity
    when it's deleted from the system. It converts the entity to archive
    data and stores it for historical tracking.

    Attributes:
        repository: Archive repository for data persistence

    Example:
        >>> use_case = ArchiveEntityUseCase(repository)
        >>> restaurant = Restaurant(id="123", name="Pizza Hut", ...)
        >>> archive = await use_case.execute(
        ...     table_name="restaurants",
        ...     entity=restaurant,
        ...     note="Restaurant closed",
        ...     deleted_by="user123",
        ... )
    """

    def __init__(self, repository: ArchiveRepositoryInterface) -> None:
        """Initialize the use case.

        Args:
            repository: Archive repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        table_name: str,
        entity: BaseModel,
        note: str | None = None,
        deleted_by: str | None = None,
        commit: bool = True,
    ) -> Archive:
        """Execute the archive entity use case.

        Converts any Pydantic entity to archive data and stores it
        in the archive table for historical tracking.

        Args:
            table_name: Name of the source table (e.g., "restaurants")
            entity: The entity being deleted (must have 'id' field)
            note: Optional note explaining why it was deleted
            deleted_by: ULID of the user who deleted the record
            commit: Whether to commit the transaction (default: True).
                    Set to False when using Unit of Work pattern.

        Returns:
            Archive: The created archive record with all metadata

        Raises:
            AttributeError: If entity doesn't have an 'id' field

        Example:
            >>> restaurant = Restaurant(
            ...     id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            ...     name="Pizza Hut",
            ...     address="123 Main St",
            ... )
            >>> archive = await use_case.execute(
            ...     table_name="restaurants",
            ...     entity=restaurant,
            ...     note="Permanently closed",
            ...     deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0",
            ... )
        """
        # Validate entity has ID
        if not hasattr(entity, "id"):
            raise AttributeError("Entity must have an 'id' field to be archived")

        # Convert entity to dict for storage
        entity_data: dict[str, Any] = entity.model_dump(mode="json")

        # Create archive data
        archive_data = ArchiveData(
            original_table=table_name,
            original_id=str(entity.id),
            data=entity_data,
            note=note,
        )

        # Persist using repository
        return await self.repository.create(
            archive_data, deleted_by=deleted_by, commit=commit
        )
