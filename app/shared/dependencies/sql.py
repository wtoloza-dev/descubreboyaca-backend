"""SQL client dependency factories with app-specific configuration.

This module provides factory functions that inject the application's
specific database configuration (from settings) into the generic
client factories from app.clients.sql.dependencies.

This is the layer that makes clients app-aware by providing concrete
configuration values and handles switching between SQLite (local) and
PostgreSQL (production) based on SCOPE.
"""

from collections.abc import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from app.clients.sql.dependencies.sqlite import (
    create_async_sqlite_session_dependency,
)
from app.core.settings import settings


async def get_async_sqlite_session_dependency() -> AsyncGenerator[AsyncSession]:
    """Dependency to get an async SQLite session (for local development).

    This dependency uses the application's configuration from settings.

    Yields:
        AsyncSession: Async SQLite session configured for the application

    Example:
        >>> @app.get("/restaurants")
        >>> async def get_restaurants(
        ...     session: AsyncSession = Depends(get_async_sqlite_session_dependency),
        ... ):
        ...     result = await session.exec(select(Restaurant))
        ...     return result.all()
    """
    async for session in create_async_sqlite_session_dependency(
        database_url="sqlite+aiosqlite:///./local.db",
        echo=settings.DEBUG,
    ):
        yield session


async def get_async_postgresql_session_dependency() -> AsyncGenerator[AsyncSession]:
    """Dependency to get an async PostgreSQL session (for production).

    This dependency uses the application's configuration from settings.
    Currently not implemented - placeholder for future PostgreSQL support.

    Yields:
        AsyncSession: Async PostgreSQL session configured for the application

    Raises:
        NotImplementedError: PostgreSQL support not yet implemented
    """
    raise NotImplementedError("PostgreSQL session dependency not yet implemented")


async def get_async_session_dependency() -> AsyncGenerator[AsyncSession]:
    """Dependency to get an async database session based on environment.

    Automatically selects the appropriate database implementation:
    - SCOPE=local → SQLite
    - SCOPE=staging/prod → PostgreSQL

    This is the main dependency that should be used throughout the application.
    It follows the Dependency Inversion Principle by providing the concrete
    implementation based on configuration.

    Yields:
        AsyncSession: Async database session for the current environment

    Example:
        >>> @app.get("/restaurants")
        >>> async def get_restaurants(
        ...     session: AsyncSession = Depends(get_async_session_dependency),
        ... ):
        ...     result = await session.exec(select(Restaurant))
        ...     return result.all()
    """
    if settings.SCOPE == "local":
        async for session in get_async_sqlite_session_dependency():
            yield session
    else:
        # For staging/production, use PostgreSQL
        async for session in get_async_postgresql_session_dependency():
            yield session
