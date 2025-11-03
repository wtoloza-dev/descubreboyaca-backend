"""Common SQL repository implementation for Archive.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.domain.entities import Archive, ArchiveData
from app.domains.audit.models import ArchiveModel


class SQLArchiveRepository:
    """Common SQL implementation for Archive repository (synchronous).

    This repository provides synchronous CRUD operations for Archive entities
    using SQLAlchemy/SQLModel. It handles the conversion between infrastructure
    models (ORM) and domain entities following DDD principles.

    Database-specific implementations (MySQL, SQLite, PostgreSQL) inherit from this
    class and can override methods if needed for specific database behavior.

    Responsibilities:
    - Execute synchronous database queries using SQLModel
    - Convert ORM models to domain entities
    - Handle database-specific logic (transactions, error handling)

    Note: This is the synchronous implementation. For async operations,
    use AsyncSQLArchiveRepository.

    Attributes:
        session: SQLModel session for database operations.
    """

    def __init__(self, session: Session) -> None:
        """Initialize the SQL repository with a database session.

        Args:
            session: SQLModel session for database operations.
        """
        self.session = session

    def create(
        self, archive_data: ArchiveData, deleted_by: str | None = None
    ) -> Archive:
        """Create a new archive record.

        Args:
            archive_data: Core archive data without system metadata.
            deleted_by: ULID of the user who deleted the record.

        Returns:
            Archive: Complete archive entity with ID and system metadata.

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


class AsyncSQLArchiveRepository:
    """Common SQL implementation for Archive repository (asynchronous).

    This repository provides async CRUD operations for Archive entities using
    SQLAlchemy/SQLModel with async/await support. It handles the conversion
    between infrastructure models (ORM) and domain entities following DDD principles.

    Database-specific implementations (MySQL, SQLite, PostgreSQL) inherit from this
    class and can override methods if needed for specific database behavior.

    Responsibilities:
    - Execute async database queries using SQLModel
    - Convert ORM models to domain entities
    - Handle database-specific logic (transactions, error handling)

    Note: This repository is used for async operations and supports the
    commit parameter for Unit of Work pattern (Archive Pattern requirement).

    Attributes:
        session: Async SQLAlchemy session for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the async SQL repository with an async database session.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self.session = session

    async def create(
        self,
        archive_data: ArchiveData,
        deleted_by: str | None = None,
        commit: bool = True,
    ) -> Archive:
        """Create a new archive record asynchronously.

        This method supports the Archive Pattern by allowing commit=False
        for atomic operations with Unit of Work.

        Args:
            archive_data: Core archive data without system metadata.
            deleted_by: ULID of the user who deleted the record.
            commit: Whether to commit the transaction (default: True).
                    Set to False when using Unit of Work pattern.

        Returns:
            Archive: Complete archive entity with ID and system metadata.

        Example:
            >>> # Standard usage
            >>> data = ArchiveData(
            ...     original_table="restaurants",
            ...     original_id="01ARZ3NDEKTSV4RRFFQ69G5FAV",
            ...     data={"name": "Pizza Hut", "address": "..."},
            ...     note="Closed permanently",
            ... )
            >>> archive = await repo.create(
            ...     data, deleted_by="01BX5ZZKBKACTAV9WEVGEMMVS0"
            ... )

            >>> # Archive Pattern usage (atomic with delete)
            >>> archive = await repo.create(data, deleted_by=user_id, commit=False)
            >>> await entity_repo.delete(id, commit=False)
            >>> await uow.commit()  # Both succeed or fail together
        """
        # Create entity - it generates its own ID and timestamps (DDD)
        archive = Archive(**archive_data.model_dump(), deleted_by=deleted_by)

        # Convert to model and persist
        model = ArchiveModel.model_validate(archive)
        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)
        else:
            # When not committing (UoW pattern), flush to get DB-generated values
            await self.session.flush()

        # Return as entity
        return Archive.model_validate(model)

    async def commit(self) -> None:
        """Commit the current transaction.

        Commits all pending changes in the current database session.
        """
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Rolls back all pending changes in the current database session.
        """
        await self.session.rollback()
