"""Archive repository interfaces.

This module defines the interface contracts for Archive repository operations.
Both synchronous and asynchronous versions are provided.
"""

from typing import Protocol

from app.shared.domain import Archive, ArchiveData


class ArchiveRepositoryInterface(Protocol):
    """Interface defining the contract for synchronous Archive repository.

    This interface defines the operations that can be performed on
    archived records storage using synchronous operations.
    """

    def create(
        self, archive_data: ArchiveData, deleted_by: str | None = None
    ) -> Archive:
        """Create a new archive record.

        Args:
            archive_data: Core archive data without system metadata
            deleted_by: ULID of the user who deleted the record

        Returns:
            Archive: Complete archive entity with ID and system metadata

        Example:
            >>> data = ArchiveData(
            ...     original_table="restaurants",
            ...     original_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            ...     data={"name": "Pizza Hut", "address": "..."},
            ...     note="Closed permanently",
            ... )
            >>> archive = repo.create(data, deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0")
        """
        ...


class AsyncArchiveRepositoryInterface(Protocol):
    """Interface defining the contract for asynchronous Archive repository.

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
