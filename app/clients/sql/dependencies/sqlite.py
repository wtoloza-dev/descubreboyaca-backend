"""SQLite adapter factory functions.

This module provides generic factory functions to create SQLite adapter instances.
These factories are app-agnostic and accept all configuration as parameters.

These adapters are typically created once during application startup in the lifespan
and shared across all requests for optimal connection pooling.

For session dependencies, use get_session/get_async_session from app.shared.dependencies.sql
"""

from app.clients.sql.adapters import (
    AsyncSQLiteAdapter,
    SQLiteAdapter,
)


def create_sqlite_adapter(database_url: str, echo: bool = False) -> SQLiteAdapter:
    """Create a SQLite synchronous adapter instance.

    Args:
        database_url: SQLite database URL (e.g., "sqlite:///./database.db")
        echo: Whether to echo SQL statements (useful for debugging)

    Returns:
        SQLiteAdapter: Configured SQLite synchronous adapter

    Example:
        >>> adapter = create_sqlite_adapter("sqlite:///./test.db", echo=True)
        >>> with adapter.get_session() as session:
        ...     restaurants = session.exec(select(Restaurant)).all()
    """
    return SQLiteAdapter(database_url=database_url, echo=echo)


def create_async_sqlite_adapter(
    database_url: str, echo: bool = False
) -> AsyncSQLiteAdapter:
    """Create an async SQLite adapter instance.

    Args:
        database_url: SQLite database URL with async driver
            (e.g., "sqlite+aiosqlite:///./database.db")
        echo: Whether to echo SQL statements (useful for debugging)

    Returns:
        AsyncSQLiteAdapter: Configured async SQLite adapter

    Example:
        >>> adapter = create_async_sqlite_adapter(
        ...     "sqlite+aiosqlite:///./test.db", echo=True
        ... )
        >>> async with adapter.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
    """
    return AsyncSQLiteAdapter(database_url=database_url, echo=echo)
