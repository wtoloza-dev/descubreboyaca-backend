"""Archive repository implementations.

This module provides synchronous and asynchronous implementations
of the Archive repository for data persistence.
"""

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shared.domain import Archive, ArchiveData
from app.shared.models import ArchiveModel


class ArchiveRepositoryPostgreSQL:
    """Synchronous archive repository implementation.

    Handles persistence of archived records using SQLModel with
    synchronous database operations.

    Attributes:
        session: SQLModel session for database operations

    Example:
        >>> repo = ArchiveRepository(session)
        >>> data = ArchiveData(
        ...     original_table="restaurants",
        ...     original_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        ...     data={"name": "Pizza Hut"},
        ...     note="Closed permanently",
        ... )
        >>> archive = repo.create(data, deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0")
    """

    def __init__(self, session: Session) -> None:
        """Initialize the archive repository.

        Args:
            session: SQLModel session for database operations
        """
        self.session = session

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
        # Create entity - it generates its own ID and timestamps (DDD)
        archive = Archive(**archive_data.model_dump(), deleted_by=deleted_by)

        # Convert to model and persist
        model = ArchiveModel.model_validate(archive)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        # Return as entity
        return Archive.model_validate(model)


class AsyncArchiveRepositoryPostgreSQL:
    """Asynchronous archive repository implementation.

    Handles persistence of archived records using SQLModel with
    asynchronous database operations.

    Attributes:
        session: SQLModel async session for database operations

    Example:
        >>> repo = AsyncArchiveRepository(async_session)
        >>> data = ArchiveData(
        ...     original_table="restaurants",
        ...     original_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
        ...     data={"name": "Pizza Hut"},
        ...     note="Closed permanently",
        ... )
        >>> archive = await repo.create(data, deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0")
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the async archive repository.

        Args:
            session: SQLModel async session for database operations
        """
        self.session = session

    async def create(
        self, archive_data: ArchiveData, deleted_by: str | None = None
    ) -> Archive:
        """Create a new archive record asynchronously.

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
            >>> archive = await repo.create(
            ...     data, deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0"
            ... )
        """
        # Create entity - it generates its own ID and timestamps (DDD)
        archive = Archive(**archive_data.model_dump(), deleted_by=deleted_by)

        # Convert to model and persist
        model = ArchiveModel.model_validate(archive)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        # Return as entity
        return Archive.model_validate(model)
