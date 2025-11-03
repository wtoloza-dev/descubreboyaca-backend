"""Application lifespan management.

This module handles application startup and shutdown events using FastAPI's
lifespan context manager pattern for proper resource management.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.sql import create_async_sqlite_adapter, create_sqlite_adapter
from app.core.settings import settings


# Global adapter instances
_sync_adapter = None
_async_adapter = None


def get_sync_adapter():
    """Get the synchronous database adapter instance.

    Returns:
        SQLiteSynchronousAdapter: The shared sync adapter instance

    Raises:
        RuntimeError: If called before application startup
    """
    if _sync_adapter is None:
        msg = "Sync adapter not initialized. Call during application lifespan."
        raise RuntimeError(msg)
    return _sync_adapter


def get_async_adapter():
    """Get the asynchronous database adapter instance.

    Returns:
        SQLiteAsynchronousAdapter: The shared async adapter instance

    Raises:
        RuntimeError: If called before application startup
    """
    if _async_adapter is None:
        msg = "Async adapter not initialized. Call during application lifespan."
        raise RuntimeError(msg)
    return _async_adapter


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Manage application lifespan with proper resource initialization and cleanup.

    This context manager handles:
    - Database engine initialization on startup
    - Engine disposal on shutdown (automatic via SQLAlchemy)

    Args:
        app: FastAPI application instance

    Yields:
        None: Control flow during application runtime

    Example:
        >>> app = FastAPI(lifespan=lifespan)
    """
    global _sync_adapter, _async_adapter

    # Startup: Initialize database adapters
    _sync_adapter = create_sqlite_adapter(
        database_url=settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
    )

    _async_adapter = create_async_sqlite_adapter(
        database_url=settings.DATABASE_ASYNC_URL,
        echo=settings.DATABASE_ECHO,
    )

    # Yield control to the application
    yield

    # Shutdown: Dispose of engines
    # SQLAlchemy engines automatically clean up connections on disposal
    _sync_adapter.engine.dispose()
    await _async_adapter.engine.dispose()

    # Reset global references
    _sync_adapter = None
    _async_adapter = None
