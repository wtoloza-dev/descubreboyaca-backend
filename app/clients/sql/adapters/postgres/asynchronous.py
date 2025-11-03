"""PostgreSQL asynchronous database adapter (Adapter).

This module provides asynchronous implementation for PostgreSQL databases.
This is an ADAPTER in Hexagonal Architecture.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class PostgreSQLAsynchronousAdapter:
    """PostgreSQL asynchronous database adapter implementation.

    This adapter implements the AsyncSQLClientPort for PostgreSQL databases.
    It handles async connection management and session lifecycle with connection pooling.

    All database operations should be performed asynchronously using
    the async session in repositories.

    Attributes:
        engine: SQLAlchemy async engine for database connections
        async_session: Async session maker

    Example:
        >>> url = "postgresql+asyncpg://user:pass@localhost/dbname"
        >>> adapter = PostgreSQLAsynchronousAdapter(url)
        >>> async with adapter.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
        ...     restaurants = result.all()
    """

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize async PostgreSQL adapter.

        Args:
            database_url: PostgreSQL database URL with async driver
                Format: "postgresql+asyncpg://username:password@host:port/database"
            echo: Whether to echo SQL statements (useful for debugging)

        Example:
            >>> url = "postgresql+asyncpg://user:pass@localhost:5432/mydb"
            >>> adapter = PostgreSQLAsynchronousAdapter(url, echo=True)
        """
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            echo=echo,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
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
