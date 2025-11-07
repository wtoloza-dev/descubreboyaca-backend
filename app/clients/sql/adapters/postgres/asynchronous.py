"""PostgreSQL asynchronous database adapter (Adapter).

This module provides asynchronous implementation for PostgreSQL databases.
This is an ADAPTER in Hexagonal Architecture.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncPostgreSQLAdapter:
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
        >>> adapter = AsyncPostgreSQLAdapter(url)
        >>> adapter.connect()
        >>> async with adapter.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
        ...     restaurants = result.all()
    """

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_recycle: int = 3600,
        pool_pre_ping: bool = True,
    ) -> None:
        """Initialize async PostgreSQL adapter.

        Args:
            database_url: PostgreSQL database URL with async driver
                Format: "postgresql+asyncpg://username:password@host:port/database"
            echo: Whether to echo SQL statements (useful for debugging)
            pool_size: Number of permanent connections in the pool (default: 5)
            max_overflow: Maximum additional connections allowed (default: 10)
            pool_recycle: Recycle connections after N seconds (default: 3600)
            pool_pre_ping: Verify connection before using (default: True)

        Example:
            >>> url = "postgresql+asyncpg://user:pass@localhost:5432/mydb"
            >>> adapter = PostgreSQLAsyncAdapter(
            ...     url, echo=True, pool_size=10, max_overflow=20
            ... )
        """
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            echo=echo,
            pool_pre_ping=pool_pre_ping,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
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
