"""Archive repository interfaces.

This module defines the interface contracts for Archive repository operations.
All operations are asynchronous by default.
"""

from typing import Any, Protocol

from app.domains.audit.domain.entities import Archive, ArchiveData


class ArchiveRepositoryInterface(Protocol):
    """Interface defining the contract for Archive repository.

    This interface defines the operations that can be performed on
    archived records storage using asynchronous operations.
    """

    async def create(
        self,
        archive_data: ArchiveData,
        deleted_by: str | None = None,
        commit: bool = True,
    ) -> Archive:
        """Create a new archive record asynchronously.

        Args:
            archive_data: Core archive data without system metadata
            deleted_by: ULID of the user who deleted the record
            commit: Whether to commit the transaction (default: True).
                    Set to False when using Unit of Work pattern.

        Returns:
            Archive: Complete archive entity with ID and system metadata

        Example:
            >>> data = ArchiveData(
            ...     original_table="restaurants",
            ...     original_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            ...     data={"name": "Pizza Hut", "address": "..."},
            ...     note="Closed permanently",
            ... )
            >>> archive = await repo.create(
            ...     data, deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0"
            ... )
        """
        ...

    async def commit(self) -> None:
        """Commit the current transaction.

        Commits all pending changes in the current database session.
        """
        ...

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Rolls back all pending changes in the current database session.
        """
        ...

    async def find(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Archive]:
        """Find archive records with dynamic filters and pagination.

        This method allows querying archives with any combination of filters
        by dynamically building the WHERE clause using model attributes.

        Args:
            filters: Dictionary of field names and their values to filter by.
                     Keys should match ArchiveModel attribute names.
                     Example: {"original_table": "restaurants", "original_id": "..."}
            offset: Number of records to offset (skip)
            limit: Maximum number of records to return

        Returns:
            List of archives matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute

        Example:
            >>> archives = await repo.find()  # Get all
            >>> archives = await repo.find({"original_table": "restaurants"})
            >>> archives = await repo.find(
            ...     {"original_table": "restaurants", "original_id": "01ARZ..."},
            ...     offset=0,
            ...     limit=10,
            ... )
        """
        ...

    async def hard_delete(
        self,
        filters: dict[str, Any],
    ) -> bool:
        """Hard delete an archive record by filters.

        Args:
            filters: Dictionary with filter criteria.
                     Keys should match ArchiveModel attribute names.
                     Example: {"original_table": "restaurants", "original_id": "..."}

        Returns:
            bool: True if an archive was deleted, False if not found

        Raises:
            AttributeError: If a filter key doesn't match any model attribute

        Example:
            >>> deleted = await repo.hard_delete(
            ...     {
            ...         "original_table": "restaurants",
            ...         "original_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
            ...     }
            ... )
        """
        ...
