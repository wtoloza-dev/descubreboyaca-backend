"""Archive business services.

This module provides services for archiving deleted records.
Services coordinate between repositories and contain business logic.

This is part of the Audit domain and will be extended in the future
with complete audit logging (see project/AUDIT_SYSTEM_PROPOSAL.md).
"""

from typing import Any

from pydantic import BaseModel

from app.domains.audit.domain import (
    Archive,
    ArchiveData,
    ArchiveRepositoryInterface,
    AsyncArchiveRepositoryInterface,
)


class ArchiveService:
    """Synchronous archive service for managing deleted records.

    This service provides business logic for archiving any entity
    when it's deleted from the system.

    Attributes:
        repository: Archive repository for data persistence

    Example:
        >>> service = ArchiveService(repository)
        >>> restaurant = Restaurant(id="123", name="Pizza Hut", ...)
        >>> archive = service.archive_entity(
        ...     table_name="restaurants",
        ...     entity=restaurant,
        ...     note="Restaurant closed",
        ...     deleted_by="user123",
        ... )
    """

    def __init__(self, repository: ArchiveRepositoryInterface) -> None:
        """Initialize archive service.

        Args:
            repository: Archive repository implementation
        """
        self.repository = repository

    def archive_entity(
        self,
        table_name: str,
        entity: BaseModel,
        note: str | None = None,
        deleted_by: str | None = None,
    ) -> Archive:
        """Archive an entity that is being deleted.

        Converts any Pydantic entity to archive data and stores it
        in the archive table for historical tracking.

        Args:
            table_name: Name of the source table (e.g., "restaurants")
            entity: The entity being deleted (must have 'id' field)
            note: Optional note explaining why it was deleted
            deleted_by: ULID of the user who deleted the record

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
            >>> archive = service.archive_entity(
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
        return self.repository.create(archive_data, deleted_by=deleted_by)


class AsyncArchiveService:
    """Asynchronous archive service for managing deleted records.

    This service provides async business logic for archiving any entity
    when it's deleted from the system.

    Attributes:
        repository: Async archive repository for data persistence

    Example:
        >>> service = AsyncArchiveService(repository)
        >>> restaurant = Restaurant(id="123", name="Pizza Hut", ...)
        >>> archive = await service.archive_entity(
        ...     table_name="restaurants",
        ...     entity=restaurant,
        ...     note="Restaurant closed",
        ...     deleted_by="user123",
        ... )
    """

    def __init__(self, repository: AsyncArchiveRepositoryInterface) -> None:
        """Initialize async archive service.

        Args:
            repository: Async archive repository implementation
        """
        self.repository = repository

    async def archive_entity(
        self,
        table_name: str,
        entity: BaseModel,
        note: str | None = None,
        deleted_by: str | None = None,
    ) -> Archive:
        """Archive an entity that is being deleted asynchronously.

        Converts any Pydantic entity to archive data and stores it
        in the archive table for historical tracking.

        Args:
            table_name: Name of the source table (e.g., "restaurants")
            entity: The entity being deleted (must have 'id' field)
            note: Optional note explaining why it was deleted
            deleted_by: ULID of the user who deleted the record

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
            >>> archive = await service.archive_entity(
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
        return await self.repository.create(archive_data, deleted_by=deleted_by)
