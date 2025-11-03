"""SQL client adapters (Implementations).

This package contains concrete implementations of SQL client ports.
These are ADAPTERS in Hexagonal Architecture (Clean Architecture).

Each adapter implements one or more of the port interfaces defined in
the ports package.
"""

from app.clients.sql.adapters.postgres import (
    PostgreSQLAsynchronousAdapter,
    PostgreSQLSynchronousAdapter,
)
from app.clients.sql.adapters.sqlite import (
    SQLiteAsynchronousAdapter,
    SQLiteSynchronousAdapter,
)


__all__ = [
    "SQLiteSynchronousAdapter",
    "SQLiteAsynchronousAdapter",
    "PostgreSQLSynchronousAdapter",
    "PostgreSQLAsynchronousAdapter",
]
