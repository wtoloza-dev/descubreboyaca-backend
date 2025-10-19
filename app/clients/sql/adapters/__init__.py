"""SQL client adapters (Implementations).

This package contains concrete implementations of SQL client protocols.
These are ADAPTERS in Hexagonal Architecture (Clean Architecture).

Each adapter implements one or more of the protocol interfaces defined in
the interfaces package.
"""

from app.clients.sql.adapters.postgres_client import (
    AsyncPostgreSQLClient,
    PostgreSQLClient,
)
from app.clients.sql.adapters.sqlite_client import AsyncSQLiteClient, SQLiteClient


__all__ = [
    "SQLiteClient",
    "AsyncSQLiteClient",
    "PostgreSQLClient",
    "AsyncPostgreSQLClient",
]
