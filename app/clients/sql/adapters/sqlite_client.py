"""SQLite database client implementations (Adapter).

This module provides sync and async implementations of SQLClientProtocol for SQLite.
This is an ADAPTER in Hexagonal Architecture.
"""

from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import Session, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class SQLiteClient:
    """SQLite synchronous database client implementation.

    This adapter implements the SQLClientProtocol for SQLite databases.
    It handles connection management and session lifecycle.

    All database operations (queries, inserts, updates, deletes) should be
    performed directly on the session in repositories.

    Attributes:
        engine: SQLAlchemy engine for database connections

    Example:
        >>> client = SQLiteClient("sqlite:///./database.db")
        >>> with client.get_session() as session:
        ...     # Query
        ...     restaurants = session.exec(select(Restaurant)).all()
        ...     # Insert
        ...     session.add(new_restaurant)
        ...     session.commit()
    """

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize SQLite client.

        Args:
            database_url: SQLite database URL (e.g., "sqlite:///./database.db")
            echo: Whether to echo SQL statements (useful for debugging)

        Example:
            >>> client = SQLiteClient("sqlite:///./app.db", echo=True)
        """
        self.engine: Engine = create_engine(
            database_url,
            echo=echo,
            connect_args={"check_same_thread": False},  # SQLite specific
        )

    def create_db_and_tables(self) -> None:
        """Create all database tables defined in SQLModel models.

        This should be called during application startup to initialize the database.

        Example:
            >>> client = SQLiteClient("sqlite:///./app.db")
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


class AsyncSQLiteClient:
    """SQLite asynchronous database client implementation.

    This adapter implements the AsyncSQLClientProtocol for SQLite databases.
    It handles async connection management and session lifecycle.

    All database operations should be performed asynchronously using
    the async session in repositories.

    Attributes:
        engine: SQLAlchemy async engine for database connections
        async_session: Async session maker

    Example:
        >>> client = AsyncSQLiteClient("sqlite+aiosqlite:///./database.db")
        >>> async with client.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
        ...     restaurants = result.all()
    """

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize async SQLite client.

        Args:
            database_url: SQLite database URL with async driver
                Format: "sqlite+aiosqlite:///./database.db"
            echo: Whether to echo SQL statements (useful for debugging)

        Example:
            >>> client = AsyncSQLiteClient("sqlite+aiosqlite:///./app.db")
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
