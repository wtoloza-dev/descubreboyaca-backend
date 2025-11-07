"""SQL database clients (Hexagonal Architecture - Ports and Adapters).

This package implements the Ports and Adapters pattern for database clients
following modern SQLAlchemy 2.0 and FastAPI best practices.

Structure:
- ports/: PORTS (Port definitions) - defines the contracts
  - synchronous.py: Synchronous SQL client port
  - asynchronous.py: Asynchronous SQL client port

- adapters/: ADAPTERS (Implementations) - concrete implementations
  - sqlite/: SQLite adapters
    - synchronous.py: Synchronous SQLite adapter
    - asynchronous.py: Asynchronous SQLite adapter
  - postgres/: PostgreSQL adapters
    - synchronous.py: Synchronous PostgreSQL adapter
    - asynchronous.py: Asynchronous PostgreSQL adapter

- dependencies/: GENERIC FACTORIES (app-agnostic) - creates adapter instances
  - sqlite.py: Generic SQLite adapter factories that accept config as parameters

Best Practices (SQLAlchemy 2.0 + FastAPI):
    1. Engine Lifecycle: Managed via FastAPI lifespan events
       - Engines created once on startup
       - Disposed automatically on shutdown
       - No manual close() needed

    2. Connection Pooling: Handled automatically by SQLAlchemy
       - Single engine per application
       - Reused across all requests

    3. Session Management: Per-request via dependency injection
       - Use context managers for automatic cleanup
       - Sessions are short-lived (per-request)

    4. Separation: Sync and async adapters are completely separate
       - Different engines for sync/async
       - No mixing of paradigms

For app-specific dependencies with concrete configuration, use app.shared.dependencies:

Usage:
    >>> from app.shared.dependencies import get_async_session_dependency
    >>> from fastapi import Depends
    >>>
    >>> @app.get("/restaurants")
    >>> async def get_restaurants(
    ...     session: AsyncSession = Depends(get_async_session_dependency),
    ... ):
    ...     result = await session.exec(select(Restaurant))
    ...     return result.all()

Application Setup:
    >>> # In app/main.py
    >>> from app.core.lifespan import lifespan
    >>> app = FastAPI(lifespan=lifespan)
"""

from app.clients.sql.adapters import (
    AsyncPostgreSQLAdapter,
    AsyncSQLiteAdapter,
    PostgreSQLAdapter,
    SQLiteAdapter,
)
from app.clients.sql.dependencies import (
    create_async_sqlite_adapter,
    create_sqlite_adapter,
)
from app.clients.sql.ports import AsyncSQLClientPort, SQLClientPort


__all__ = [
    # Ports (Contracts)
    "SQLClientPort",
    "AsyncSQLClientPort",
    # Adapters (Implementations)
    "SQLiteAdapter",
    "AsyncSQLiteAdapter",
    "PostgreSQLAdapter",
    "AsyncPostgreSQLAdapter",
    # Generic Factories (app-agnostic)
    "create_sqlite_adapter",
    "create_async_sqlite_adapter",
]
