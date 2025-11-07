"""SQL client adapters (Implementations).

This package contains concrete implementations of SQL client ports.
These are ADAPTERS in Hexagonal Architecture (Clean Architecture).

Each adapter implements one or more of the port interfaces defined in
the ports package.
"""

from app.clients.sql.adapters.postgres import (
    AsyncPostgreSQLAdapter,
    PostgreSQLAdapter,
)
from app.clients.sql.adapters.sqlite import (
    AsyncSQLiteAdapter,
    SQLiteAdapter,
)


__all__ = [
    "SQLiteAdapter",
    "AsyncSQLiteAdapter",
    "PostgreSQLAdapter",
    "AsyncPostgreSQLAdapter",
]
