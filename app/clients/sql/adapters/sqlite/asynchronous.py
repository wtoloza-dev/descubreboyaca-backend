"""SQLite asynchronous database adapter (Adapter).

This module provides asynchronous implementation for SQLite databases.
This is an ADAPTER in Hexagonal Architecture.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncSQLiteAdapter:
    """SQLite asynchronous database adapter implementation.

    This adapter implements the AsyncSQLClientPort for SQLite databases.
    It handles async connection management and session lifecycle.

    All database operations should be performed asynchronously using
    the async session in repositories.

    Attributes:
        engine: SQLAlchemy async engine for database connections
        async_session: Async session maker

    Example:
        >>> adapter = AsyncSQLiteAdapter("sqlite+aiosqlite:///./database.db")
        >>> async with adapter.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
        ...     restaurants = result.all()
    """

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize async SQLite adapter.

        Args:
            database_url: SQLite database URL with async driver
                Format: "sqlite+aiosqlite:///./database.db"
            echo: Whether to echo SQL statements (useful for debugging)

        Example:
            >>> adapter = AsyncSQLiteAdapter("sqlite+aiosqlite:///./app.db")
        """
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            echo=echo,
            connect_args={"check_same_thread": False},
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        """Get an async database session context manager.

        Yields:
            AsyncSession: SQLModel async session for database operations

        Example:
            >>> async with adapter.get_session() as session:
            ...     result = await session.exec(select(Restaurant))
            ...     restaurant = result.first()
            ...     session.add(new_restaurant)
            ...     await session.commit()
        """
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()
