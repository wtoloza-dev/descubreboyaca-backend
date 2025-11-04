"""PostgreSQL adapter factory functions.

This module provides generic factory functions to create PostgreSQL adapter instances.
These factories are app-agnostic and accept all configuration as parameters.

These adapters are typically created once during application startup in the lifespan
and shared across all requests for optimal connection pooling.

For session dependencies, use get_session/get_async_session from app.shared.dependencies.sql
"""

from app.clients.sql.adapters import (
    PostgreSQLAsynchronousAdapter,
    PostgreSQLSynchronousAdapter,
)


def create_postgres_adapter(
    database_url: str,
    echo: bool = False,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_recycle: int = 3600,
    pool_pre_ping: bool = True,
) -> PostgreSQLSynchronousAdapter:
    """Create a PostgreSQL synchronous adapter instance.

    Args:
        database_url: PostgreSQL database URL (e.g., "postgresql://user:pass@host/db")
        echo: Whether to echo SQL statements (useful for debugging)
        pool_size: Number of permanent connections in the pool (default: 5)
        max_overflow: Maximum additional connections allowed (default: 10)
        pool_recycle: Recycle connections after N seconds (default: 3600)
        pool_pre_ping: Verify connection before using (default: True)

    Returns:
        PostgreSQLSynchronousAdapter: Configured PostgreSQL synchronous adapter

    Example:
        >>> adapter = create_postgres_adapter(
        ...     "postgresql://user:pass@localhost:5432/mydb",
        ...     echo=True,
        ...     pool_size=10,
        ...     max_overflow=20,
        ... )
        >>> with adapter.get_session() as session:
        ...     restaurants = session.exec(select(Restaurant)).all()
    """
    return PostgreSQLSynchronousAdapter(
        database_url=database_url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_recycle=pool_recycle,
        pool_pre_ping=pool_pre_ping,
    )


def create_async_postgres_adapter(
    database_url: str,
    echo: bool = False,
    pool_size: int = 5,
    max_overflow: int = 10,
    pool_recycle: int = 3600,
    pool_pre_ping: bool = True,
) -> PostgreSQLAsynchronousAdapter:
    """Create an async PostgreSQL adapter instance.

    Args:
        database_url: PostgreSQL database URL with async driver
            (e.g., "postgresql+asyncpg://user:pass@host:5432/db")
        echo: Whether to echo SQL statements (useful for debugging)
        pool_size: Number of permanent connections in the pool (default: 5)
        max_overflow: Maximum additional connections allowed (default: 10)
        pool_recycle: Recycle connections after N seconds (default: 3600)
        pool_pre_ping: Verify connection before using (default: True)

    Returns:
        PostgreSQLAsynchronousAdapter: Configured async PostgreSQL adapter

    Example:
        >>> adapter = create_async_postgres_adapter(
        ...     "postgresql+asyncpg://user:pass@localhost:5432/mydb",
        ...     echo=True,
        ...     pool_size=10,
        ...     max_overflow=20,
        ... )
        >>> async with adapter.get_session() as session:
        ...     result = await session.exec(select(Restaurant))
    """
    return PostgreSQLAsynchronousAdapter(
        database_url=database_url,
        echo=echo,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_recycle=pool_recycle,
        pool_pre_ping=pool_pre_ping,
    )
