"""Hard delete archive by original ID use case.

This module contains the use case for permanently deleting an archive record
from the database.
"""

from app.domains.audit.domain import ArchiveRepositoryInterface


class HardDeleteArchiveByOriginalIdUseCase:
    """Use case for permanently deleting an archive record.

    This is an admin-only operation that permanently removes an archive
    record from the database. Use with caution as this is irreversible.

    Attributes:
        repository: Archive repository for data persistence

    Example:
        >>> use_case = HardDeleteArchiveByOriginalIdUseCase(repository)
        >>> deleted = await use_case.execute(
        ...     original_table="restaurants",
        ...     original_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
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
        original_table: str,
        original_id: str,
    ) -> bool:
        """Execute the hard delete archive use case.

        This operation permanently removes an archive record from the
        database based on the original table name and ID.

        Args:
            original_table: Name of the source table (e.g., "restaurants")
            original_id: ID from the original record

        Returns:
            bool: True if the archive was deleted, False if not found

        Example:
            >>> deleted = await use_case.execute(
            ...     original_table="restaurants",
            ...     original_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            ... )
            >>> if deleted:
            ...     print("Archive permanently deleted")
        """
        filters = {
            "original_table": original_table,
            "original_id": original_id,
        }
        return await self.repository.hard_delete(filters)
