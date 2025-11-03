"""SQLite adapter dependency factories.

This module provides generic factory functions to create SQLite adapter instances
and session dependencies. These factories are app-agnostic and accept all
configuration as parameters.

For app-specific configurations, use the factories in app.shared.dependencies.
"""

from collections.abc import AsyncGenerator, Generator

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.clients.sql.adapters import (
    SQLiteAsynchronousAdapter,
    SQLiteSynchronousAdapter,
)


def create_sqlite_adapter(
    database_url: str, echo: bool = False
) -> SQLiteSynchronousAdapter:
    """Create a SQLite synchronous adapter instance.

    Args:
        database_url: SQLite database URL (e.g., "sqlite:///./database.db")
        echo: Whether to echo SQL statements (useful for debugging)

    Returns:
        SQLiteSynchronousAdapter: Configured SQLite synchronous adapter

    Example:
        >>> adapter = create_sqlite_adapter("sqlite:///./test.db", echo=True)
        >>> with adapter.get_session() as session:
        ...     restaurants = session.exec(select(Restaurant)).all()
    """
    return SQLiteSynchronousAdapter(database_url=database_url, echo=echo)


def create_async_sqlite_adapter(
    database_url: str, echo: bool = False
) -> SQLiteAsynchronousAdapter:
    """Create an async SQLite adapter instance.

    Args:
        database_url: SQLite database URL with async driver
            (e.g., "sqlite+aiosqlite:///./database.db")
        echo: Whether to echo SQL statements (useful for debugging)

    Returns:
        SQLiteAsynchronousAdapter: Configured async SQLite adapter

    Example:
        >>> adapter = create_async_sqlite_adapter(
        ...     "sqlite+aiosqlite:///./test.db", echo=True
        ... )
        >>> async with adapter.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
    """
    return SQLiteAsynchronousAdapter(database_url=database_url, echo=echo)


def create_sqlite_session_dependency(
    database_url: str, echo: bool = False
) -> Generator[Session]:
    """Create a dependency factory for SQLite sessions.

    Args:
        database_url: SQLite database URL (e.g., "sqlite:///./database.db")
        echo: Whether to echo SQL statements (useful for debugging)

    Yields:
        Session: SQLite session for database operations

    Example:
        >>> # In your app-specific dependencies:
        >>> def get_session() -> Generator[Session, None, None]:
        ...     yield from create_sqlite_session_dependency(
        ...         "sqlite:///./test.db", echo=True
        ...     )
        >>>
        >>> @app.get("/restaurants")
        >>> def get_restaurants(session: Session = Depends(get_session)):
        ...     return session.exec(select(Restaurant)).all()
    """
    adapter = create_sqlite_adapter(database_url=database_url, echo=echo)
    with adapter.get_session() as session:
        yield session


async def create_async_sqlite_session_dependency(
    database_url: str, echo: bool = False
) -> AsyncGenerator[AsyncSession]:
    """Create a dependency factory for async SQLite sessions.

    Args:
        database_url: SQLite database URL with async driver
            (e.g., "sqlite+aiosqlite:///./database.db")
        echo: Whether to echo SQL statements (useful for debugging)

    Yields:
        AsyncSession: Async SQLite session for database operations

    Example:
        >>> # In your app-specific dependencies:
        >>> async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        ...     async for session in create_async_sqlite_session_dependency(
        ...         "sqlite+aiosqlite:///./test.db", echo=True
        ...     ):
        ...         yield session
        >>>
        >>> @app.get("/restaurants")
        >>> async def get_restaurants(
        ...     session: AsyncSession = Depends(get_async_session),
        ... ):
        ...     result = await session.exec(select(Restaurant))
        ...     return result.all()
    """
    adapter = create_async_sqlite_adapter(database_url=database_url, echo=echo)
    async with adapter.get_session() as session:
        yield session
