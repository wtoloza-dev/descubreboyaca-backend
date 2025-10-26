"""Unit of Work pattern implementation.

This module implements the Unit of Work pattern for managing database transactions.

The Unit of Work pattern maintains a list of objects affected by a business transaction
and coordinates the writing of changes, ensuring atomicity.

Key benefits:
- Atomicity: All changes succeed or all fail (no partial commits)
- Consistency: Related changes happen together
- Simplified transaction management: One commit point
- Testability: Easy to mock and test
"""

from typing import Protocol

from sqlmodel.ext.asyncio.session import AsyncSession


class UnitOfWorkInterface(Protocol):
    """Interface for Unit of Work pattern.

    This protocol defines the contract for managing a unit of work (transaction).
    Repositories within the same UoW share the same session and transaction.
    """

    async def commit(self) -> None:
        """Commit all changes in the current transaction.

        All repository operations within this UoW will be persisted atomically.
        Either all succeed or all fail.
        """
        ...

    async def rollback(self) -> None:
        """Rollback all changes in the current transaction.

        Discards all pending changes. Useful for error handling.
        """
        ...

    async def __aenter__(self) -> UnitOfWorkInterface:
        """Enter async context manager."""
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager.

        Automatically rolls back if an exception occurred.
        """
        ...


class AsyncUnitOfWork:
    """Async Unit of Work implementation for SQLModel.

    This class manages a database transaction across multiple repositories.
    All repositories created within the same UoW share the same session,
    ensuring atomicity of operations.

    Attributes:
        session: SQLModel async session for database operations

    Example:
        >>> async with AsyncUnitOfWork(session) as uow:
        ...     # All operations share the same transaction
        ...     restaurant = await uow.restaurant_repo.create(data, commit=False)
        ...     archive = await uow.archive_repo.create(data, commit=False)
        ...     await uow.commit()  # Single atomic commit

    Key Concepts:
        - **Transaction boundary**: UoW defines where transaction starts/ends
        - **Shared session**: All repos use same session = same transaction
        - **Explicit commit**: Developer controls when to commit
        - **Auto-rollback**: Exception = automatic rollback
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize Unit of Work with a database session.

        Args:
            session: SQLModel async session for database operations

        Note:
            The session should be a single instance shared across all repositories
            to ensure they participate in the same transaction.
        """
        self.session = session
        self._committed = False

    async def commit(self) -> None:
        """Commit all changes in the current transaction.

        This persists all pending changes from all repositories that
        used this UoW's session. Either all changes succeed or all fail.

        Example:
            >>> async with AsyncUnitOfWork(session) as uow:
            ...     await repo1.create(data, commit=False)  # Pending
            ...     await repo2.delete(id, commit=False)  # Pending
            ...     await uow.commit()  # Both persisted atomically

        Raises:
            Exception: If commit fails, propagates database exception
        """
        await self.session.commit()
        self._committed = True

    async def rollback(self) -> None:
        """Rollback all changes in the current transaction.

        Discards all pending changes. This is typically called automatically
        when an exception occurs, but can also be called explicitly.

        Example:
            >>> async with AsyncUnitOfWork(session) as uow:
            ...     try:
            ...         await repo.create(data, commit=False)
            ...         if not valid:
            ...             await uow.rollback()
            ...             return
            ...         await uow.commit()
            ...     except Exception:
            ...         # Auto-rollback happens here
            ...         raise
        """
        await self.session.rollback()

    async def __aenter__(self) -> AsyncUnitOfWork:
        """Enter async context manager.

        Returns:
            Self: The UoW instance for use in the context

        Example:
            >>> async with AsyncUnitOfWork(session) as uow:
            ...     # uow is available here
            ...     await uow.commit()
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager with automatic cleanup.

        If an exception occurred (exc_type is not None), automatically
        rolls back the transaction. Otherwise, does nothing (you must
        call commit() explicitly).

        Args:
            exc_type: Exception type if exception occurred
            exc_val: Exception value if exception occurred
            exc_tb: Exception traceback if exception occurred

        Note:
            This does NOT auto-commit on success. You must call commit()
            explicitly. This is by design to avoid accidental commits.

        Example:
            >>> async with AsyncUnitOfWork(session) as uow:
            ...     await repo.create(data, commit=False)
            ...     # Exception here = auto-rollback
            ...     await uow.commit()  # Must be explicit
        """
        if exc_type is not None and not self._committed:
            # Exception occurred and we haven't committed yet
            await self.rollback()
        # Note: We do NOT auto-commit on success
        # This is intentional - commit must be explicit


class UnitOfWorkFactory:
    """Factory for creating Unit of Work instances.

    This factory provides a convenient way to create UoW instances
    with the correct session and configuration.

    Example:
        >>> factory = UnitOfWorkFactory()
        >>> async with factory.create(session) as uow:
        ...     # Use uow
        ...     await uow.commit()
    """

    @staticmethod
    def create(session: AsyncSession) -> AsyncUnitOfWork:
        """Create a new Unit of Work instance.

        Args:
            session: Async database session

        Returns:
            AsyncUnitOfWork: New UoW instance

        Example:
            >>> uow = UnitOfWorkFactory.create(session)
            >>> async with uow:
            ...     await uow.commit()
        """
        return AsyncUnitOfWork(session)
