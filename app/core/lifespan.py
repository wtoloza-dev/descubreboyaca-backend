"""Application lifespan management.

This module manages the application lifecycle, including database connection
pool initialization and cleanup.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.sql.dependencies import (
    # Asynchronous adapters
    create_async_postgres_adapter,
    create_async_sqlite_adapter,
    # Synchronous adapters
    create_postgres_adapter,
    create_sqlite_adapter,
)
from app.core.settings import settings
from app.shared.dependencies import get_metrics_client_dependency


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Manage application lifespan events.

    This function handles:
    - STARTUP: Initialize database connection pools based on SCOPE
    - SHUTDOWN: Clean up and dispose database connections

    Args:
        app: FastAPI application instance

    Yields:
        None: Control returns to the application runtime
    """
    # STARTUP: Initialize clients and adapters
    # Initialize metrics client
    app.state.metrics_client = get_metrics_client_dependency()

    # Create database adapters with connection pools
    if settings.SCOPE == "local":
        # Use SQLite for local development
        sync_driver = "sqlite"
        async_driver = "sqlite+aiosqlite"
        app.state.sync_adapter = create_sqlite_adapter(
            database_url=f"{sync_driver}:///{settings.DATABASE_DSN}",
            echo=settings.DEBUG,
        )
        app.state.async_adapter = create_async_sqlite_adapter(
            database_url=f"{async_driver}:///{settings.DATABASE_DSN}",
            echo=settings.DEBUG,
        )
    else:
        # Use PostgreSQL for staging/production
        sync_driver = "postgresql"
        async_driver = "postgresql+asyncpg"
        app.state.sync_adapter = create_postgres_adapter(
            database_url=f"{sync_driver}://{settings.DATABASE_DSN}",
            echo=settings.DEBUG,
        )
        app.state.async_adapter = create_async_postgres_adapter(
            database_url=f"{async_driver}://{settings.DATABASE_DSN}",
            echo=settings.DEBUG,
        )

    yield  # Application runs here

    # SHUTDOWN: Dispose engines and close connections
    app.state.sync_adapter.engine.dispose()
    await app.state.async_adapter.engine.dispose()
