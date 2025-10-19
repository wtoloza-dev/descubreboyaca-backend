"""SQLite client dependency factories.

This module provides factory functions to create SQLite client instances
and session dependencies for FastAPI endpoints.
"""

from collections.abc import AsyncGenerator, Generator

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.clients.sql.adapters import AsyncSQLiteClient, SQLiteClient
from app.core.settings import settings


def get_sqlite_client_dependency() -> SQLiteClient:
    """Get the SQLite client instance for the test database.

    Returns:
        SQLiteClient: Configured SQLite client for test.db

    Example:
        >>> client = get_sqlite_client_dependency()
        >>> with client.get_session() as session:
        ...     restaurants = session.exec(select(Restaurant)).all()
    """
    return SQLiteClient(
        database_url="sqlite:///./test.db",
        echo=settings.DEBUG,
    )


def get_async_sqlite_client_dependency() -> AsyncSQLiteClient:
    """Get the async SQLite client instance for the test database.

    Returns:
        AsyncSQLiteClient: Configured async SQLite client for test.db

    Example:
        >>> client = get_async_sqlite_client_dependency()
        >>> async with client.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
    """
    return AsyncSQLiteClient(
        database_url="sqlite+aiosqlite:///./test.db",
        echo=settings.DEBUG,
    )


def get_sqlite_session_dependency() -> Generator[Session]:
    """Dependency to get a SQLite session (for FastAPI endpoints).

    Yields:
        Session: SQLite session for test.db

    Example:
        >>> @app.get("/restaurants")
        >>> def get_restaurants(
        ...     session: Session = Depends(get_sqlite_session_dependency),
        ... ):
        ...     return session.exec(select(Restaurant)).all()
    """
    client = get_sqlite_client_dependency()
    with client.get_session() as session:
        yield session


async def get_async_sqlite_session_dependency() -> AsyncGenerator[AsyncSession]:
    """Dependency to get an async SQLite session (for FastAPI endpoints).

    Yields:
        AsyncSession: Async SQLite session for test.db

    Example:
        >>> @app.get("/restaurants")
        >>> async def get_restaurants(
        ...     session: AsyncSession = Depends(get_async_sqlite_session_dependency),
        ... ):
        ...     result = await session.exec(select(Restaurant))
        ...     return result.all()
    """
    client = get_async_sqlite_client_dependency()
    async with client.get_session() as session:
        yield session
