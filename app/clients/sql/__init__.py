"""SQL database clients (Hexagonal Architecture - Ports and Adapters).

This package implements the Ports and Adapters pattern for database clients.

Structure:
- ports/: PORTS (Protocol definitions) - defines the contracts
  - sql.py: Synchronous SQL client protocol
  - async_sql.py: Asynchronous SQL client protocol

- adapters/: ADAPTERS (Implementations) - concrete implementations
  - sqlite_client.py: SQLite sync + async clients
  - postgres_client.py: PostgreSQL sync + async clients

- dependencies/: FACTORIES (Dependency Injection) - creates configured instances
  - sqlite.py: SQLite client factories

Usage:
    >>> from app.clients.sql import get_sqlite_session
    >>> from fastapi import Depends
    >>>
    >>> @app.get("/restaurants")
    >>> def get_restaurants(session: Session = Depends(get_sqlite_session)):
    ...     return session.exec(select(Restaurant)).all()
"""

from app.clients.sql.adapters import (
    AsyncPostgreSQLClient,
    AsyncSQLiteClient,
    PostgreSQLClient,
    SQLiteClient,
)
from app.clients.sql.dependencies import (
    get_async_sqlite_client,
    get_async_sqlite_session,
    get_sqlite_client,
    get_sqlite_session,
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
    # Dependencies (Factories)
    "get_sqlite_client",
    "get_async_sqlite_client",
    "get_sqlite_session",
    "get_async_sqlite_session",
]
