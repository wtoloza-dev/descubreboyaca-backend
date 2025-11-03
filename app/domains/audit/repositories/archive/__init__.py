"""Archive repository implementations."""

from .common.sql import AsyncSQLArchiveRepository, SQLArchiveRepository
from .postgresql import AsyncPostgreSQLArchiveRepository, PostgreSQLArchiveRepository
from .sqlite import AsyncSQLiteArchiveRepository, SQLiteArchiveRepository


__all__ = [
    # Common base implementations
    "SQLArchiveRepository",
    "AsyncSQLArchiveRepository",
    # PostgreSQL implementations
    "PostgreSQLArchiveRepository",
    "AsyncPostgreSQLArchiveRepository",
    # SQLite implementations
    "SQLiteArchiveRepository",
    "AsyncSQLiteArchiveRepository",
]
