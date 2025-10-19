"""PostgreSQL database client implementations (Adapter).

This module provides sync and async implementations of SQLClientProtocol for PostgreSQL.
This is an ADAPTER in Hexagonal Architecture.
"""

from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import Session, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class PostgreSQLClient:
    """PostgreSQL synchronous database client implementation.

    This adapter implements the SQLClientProtocol for PostgreSQL databases.
    It handles connection management and session lifecycle with connection pooling.

    All database operations (queries, inserts, updates, deletes) should be
    performed directly on the session in repositories.

    Attributes:
        engine: SQLAlchemy engine for database connections

    Example:
        >>> client = PostgreSQLClient("postgresql://user:pass@localhost/dbname")
        >>> with client.get_session() as session:
        ...     # Query
        ...     restaurants = session.exec(select(Restaurant)).all()
        ...     # Insert
        ...     session.add(new_restaurant)
        ...     session.commit()
    """

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize PostgreSQL client.

        Args:
            database_url: PostgreSQL database URL
                Format: "postgresql://username:password@host:port/database"
            echo: Whether to echo SQL statements (useful for debugging)

        Example:
            >>> url = "postgresql://myuser:mypass@localhost:5432/mydb"
            >>> client = PostgreSQLClient(url, echo=True)
        """
        self.engine: Engine = create_engine(
            database_url,
            echo=echo,
            pool_pre_ping=True,  # Verify connections before using
            pool_size=5,  # Connection pool size
            max_overflow=10,  # Additional connections when pool is full
        )

    def create_db_and_tables(self) -> None:
        """Create all database tables defined in SQLModel models.

        This should be called during application startup to initialize the database.

        Example:
            >>> client = PostgreSQLClient("postgresql://...")
            >>> client.create_db_and_tables()
        """
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session]:
        """Get a database session context manager.

        Yields:
            Session: SQLModel session for database operations

        Example:
            >>> with client.get_session() as session:
            ...     restaurant = session.exec(select(Restaurant)).first()
            ...     session.add(new_restaurant)
            ...     session.commit()
        """
        session = Session(self.engine)
        try:
            yield session
        finally:
            session.close()

    def close(self) -> None:
        """Close the database connection and dispose of the engine.

        Should be called during application shutdown.

        Example:
            >>> client.close()
        """
        self.engine.dispose()


class AsyncPostgreSQLClient:
    """PostgreSQL asynchronous database client implementation.

    This adapter implements the AsyncSQLClientProtocol for PostgreSQL databases.
    It handles async connection management and session lifecycle with connection pooling.

    All database operations should be performed asynchronously using
    the async session in repositories.

    Attributes:
        engine: SQLAlchemy async engine for database connections
        async_session: Async session maker

    Example:
        >>> url = "postgresql+asyncpg://user:pass@localhost/dbname"
        >>> client = AsyncPostgreSQLClient(url)
        >>> async with client.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
        ...     restaurants = result.all()
    """

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize async PostgreSQL client.

        Args:
            database_url: PostgreSQL database URL with async driver
                Format: "postgresql+asyncpg://username:password@host:port/database"
            echo: Whether to echo SQL statements (useful for debugging)

        Example:
            >>> url = "postgresql+asyncpg://user:pass@localhost:5432/mydb"
            >>> client = AsyncPostgreSQLClient(url, echo=True)
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

    async def create_db_and_tables(self) -> None:
        """Create all database tables defined in SQLModel models.

        This should be called during application startup to initialize the database.

        Example:
            >>> await client.create_db_and_tables()
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        """Get an async database session context manager.

        Yields:
            AsyncSession: SQLModel async session for database operations

        Example:
            >>> async with client.get_session() as session:
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

    async def close(self) -> None:
        """Close the database connection and dispose of the engine.

        Should be called during application shutdown.

        Example:
            >>> await client.close()
        """
        await self.engine.dispose()
