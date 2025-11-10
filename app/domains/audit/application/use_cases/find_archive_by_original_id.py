"""Find archive by original ID use case.

This module contains the use case for finding an archive record based on
the original table name and ID.
"""

from app.domains.audit.domain import Archive, ArchiveRepositoryInterface


class FindArchiveByOriginalIdUseCase:
    """Use case for finding an archive record by original table and ID.

    This use case retrieves an archive record from the database based on
    the original table name and entity ID.

    Attributes:
        repository: Archive repository for data persistence

    Example:
        >>> use_case = FindArchiveByOriginalIdUseCase(repository)
        >>> archive = await use_case.execute(
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
    ) -> Archive | None:
        """Execute the find archive use case.

        Searches for an archive record based on the original table name
        and entity ID.

        Args:
            original_table: Name of the source table (e.g., "restaurants")
            original_id: ID from the original record

        Returns:
            Archive | None: Archive entity if found, None otherwise

        Example:
            >>> archive = await use_case.execute(
            ...     original_table="restaurants",
            ...     original_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            ... )
            >>> if archive:
            ...     print(f"Found archive: {archive.data}")
        """
        filters = {
            "original_table": original_table,
            "original_id": original_id,
        }
        archives = await self.repository.find(filters, limit=1)
        return archives[0] if archives else None
