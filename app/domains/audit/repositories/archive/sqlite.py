"""SQLite-specific implementation for Archive repository.

This module provides SQLite-specific implementation by inheriting from the
common SQL repository. Override methods here only if SQLite-specific behavior
is required.
"""

from .common.sql import AsyncSQLArchiveRepository, SQLArchiveRepository


class SQLiteArchiveRepository(SQLArchiveRepository):
    """SQLite implementation of Archive repository (synchronous).

    Inherits all operations from SQLArchiveRepository. Override methods
    here only when SQLite-specific functionality is needed, such as:
    - SQLite-specific optimizations
    - SQLite-specific query syntax
    - Custom SQLite features

    For standard operations, the inherited implementation is sufficient.
    The __init__ is automatically inherited from the parent class.

    Attributes:
        session: SQLModel session for database operations (inherited).
    """

    # SQLite-specific methods or overrides can be added here if needed
    # Most of the time, this class will be empty (just inheriting)
    pass


class AsyncSQLiteArchiveRepository(AsyncSQLArchiveRepository):
    """SQLite implementation of Archive repository (asynchronous).

    Inherits all operations from AsyncSQLArchiveRepository. Override methods
    here only when SQLite-specific functionality is needed, such as:
    - SQLite-specific async optimizations
    - SQLite-specific query syntax
    - Custom SQLite features

    For standard operations, the inherited implementation is sufficient.
    The __init__ is automatically inherited from the parent class.

    Attributes:
        session: Async SQLAlchemy session for database operations (inherited).
    """

    # SQLite-specific methods or overrides can be added here if needed
    # Most of the time, this class will be empty (just inheriting)
    pass
