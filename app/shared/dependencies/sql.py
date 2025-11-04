"""SQL client dependency factories with app-specific configuration.

This module provides dependency functions that use the database adapter
initialized during application startup via the lifespan event handler.

The adapter (SQLite or PostgreSQL) is automatically selected based on the
SCOPE environment variable and is shared across all requests for optimal
connection pooling.

Best Practice:
    Use get_async_session for all async endpoints and get_session for sync ones.
    The database adapter is initialized once during application startup
    via the lifespan event handler and shared across all requests.
    This follows the recommended pattern for SQLAlchemy connection pooling.
"""

from collections.abc import AsyncGenerator, Generator

from fastapi import Request
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from app.clients.sql.ports import AsyncSQLClientPort, SQLClientPort


def get_session_dependency(request: Request) -> Generator[Session]:
    """Get a synchronous database session dependency.

    This dependency uses the shared adapter initialized during application startup.
    The adapter automatically handles the correct database (SQLite/PostgreSQL)
    based on SCOPE and manages connection pooling and lifecycle.

    Args:
        request: FastAPI request object

    Yields:
        Session: SQLModel session for database operations

    Example:
        >>> @app.get("/restaurants")
        >>> def get_restaurants(
        ...     session: Session = Depends(get_session),
        ... ):
        ...     return session.exec(select(Restaurant)).all()
    """
    adapter: SQLClientPort = request.app.state.sync_adapter
    with adapter.get_session() as session:
        yield session


async def get_async_session_dependency(
    request: Request,
) -> AsyncGenerator[AsyncSession]:
    """Get an asynchronous database session dependency.

    This dependency uses the shared adapter initialized during application startup.
    The adapter automatically handles the correct database (SQLite/PostgreSQL)
    based on SCOPE and manages connection pooling and lifecycle.

    Args:
        request: FastAPI request object

    Yields:
        AsyncSession: Async SQLModel session for database operations

    Example:
        >>> @app.get("/restaurants")
        >>> async def get_restaurants(
        ...     session: AsyncSession = Depends(get_async_session),
        ... ):
        ...     result = await session.exec(select(Restaurant))
        ...     return result.all()
    """
    adapter: AsyncSQLClientPort = request.app.state.async_adapter
    async with adapter.get_session() as session:
        yield session
