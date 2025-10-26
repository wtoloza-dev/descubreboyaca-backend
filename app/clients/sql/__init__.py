"""SQL database clients (Hexagonal Architecture - Ports and Adapters).

This package implements the Ports and Adapters pattern for database clients.

Structure:
- ports/: PORTS (Protocol definitions) - defines the contracts
  - sql.py: Synchronous SQL client protocol
  - async_sql.py: Asynchronous SQL client protocol

- adapters/: ADAPTERS (Implementations) - concrete implementations
  - sqlite_client.py: SQLite sync + async clients
  - postgres_client.py: PostgreSQL sync + async clients

- dependencies/: GENERIC FACTORIES (app-agnostic) - creates client instances
  - sqlite.py: Generic SQLite client factories that accept config as parameters

For app-specific dependencies with concrete configuration, use app.shared.dependencies:

Usage:
    >>> from app.shared.dependencies import get_sqlite_session_dependency
    >>> from fastapi import Depends
    >>>
    >>> @app.get("/restaurants")
    >>> def get_restaurants(session: Session = Depends(get_sqlite_session_dependency)):
    ...     return session.exec(select(Restaurant)).all()
"""

from app.clients.sql.adapters import (
    AsyncPostgreSQLClient,
    AsyncSQLiteClient,
    PostgreSQLClient,
    SQLiteClient,
)
from app.clients.sql.dependencies import (
    create_async_sqlite_client,
    create_async_sqlite_session_dependency,
    create_sqlite_client,
    create_sqlite_session_dependency,
)
from app.clients.sql.ports import AsyncSQLClientProtocol, SQLClientProtocol


__all__ = [
    # Ports (Contracts)
    "SQLClientProtocol",
    "AsyncSQLClientProtocol",
    # Adapters (Implementations)
    "SQLiteClient",
    "AsyncSQLiteClient",
    "PostgreSQLClient",
    "AsyncPostgreSQLClient",
    # Generic Factories (app-agnostic)
    "create_sqlite_client",
    "create_async_sqlite_client",
    "create_sqlite_session_dependency",
    "create_async_sqlite_session_dependency",
]
