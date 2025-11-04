"""Common SQL repository implementation for Archive.

This module provides the base SQL implementation that can be shared across
different SQL databases (MySQL, SQLite, PostgreSQL). Database-specific
implementations inherit from this class and only override methods when
database-specific behavior is required.
"""

from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.domain.entities import Archive, ArchiveData
from app.domains.audit.models import ArchiveModel


class SQLArchiveRepository:
    """Common SQL implementation for Archive repository.

    This repository provides async CRUD operations for Archive entities using
    SQLAlchemy/SQLModel with async/await support. It handles the conversion
    between infrastructure models (ORM) and domain entities following DDD principles.

    Database-specific implementations (MySQL, SQLite, PostgreSQL) inherit from this
    class and can override methods if needed for specific database behavior.

    Responsibilities:
    - Execute async database queries using SQLModel
    - Convert ORM models to domain entities
    - Handle database-specific logic (transactions, error handling)

    Note: This repository supports the commit parameter for Unit of Work pattern
    (Archive Pattern requirement).

    Attributes:
        session: Async SQLAlchemy session for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the SQL repository with an async database session.

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
        statement = select(ArchiveModel)

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(ArchiveModel, field_name):
                    raise AttributeError(
                        f"ArchiveModel has no attribute '{field_name}'"
                    )

                model_field = getattr(ArchiveModel, field_name)
                statement = statement.where(model_field == value)

        # Apply ordering and pagination
        statement = (
            statement.order_by(ArchiveModel.deleted_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.exec(statement)
        models = result.all()

        return [Archive.model_validate(model) for model in models]

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
        statement = select(ArchiveModel)

        # Apply dynamic filters
        for field_name, value in filters.items():
            # Get the model attribute dynamically
            if not hasattr(ArchiveModel, field_name):
                raise AttributeError(f"ArchiveModel has no attribute '{field_name}'")

            model_field = getattr(ArchiveModel, field_name)
            statement = statement.where(model_field == value)

        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return False

        # Hard delete
        await self.session.delete(model)
        await self.session.commit()
        return True
