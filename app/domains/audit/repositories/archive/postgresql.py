"""PostgreSQL-specific implementation for Archive repository.

This module provides PostgreSQL-specific implementation by inheriting from the
common SQL repository. Override methods here only if PostgreSQL-specific behavior
is required.
"""

from .common.sql import AsyncSQLArchiveRepository, SQLArchiveRepository


class PostgreSQLArchiveRepository(SQLArchiveRepository):
    """PostgreSQL implementation of Archive repository (synchronous).

    Inherits all operations from SQLArchiveRepository. Override methods
    here only when PostgreSQL-specific functionality is needed, such as:
    - PostgreSQL-specific JSON operators
    - Full-text search
    - PostgreSQL-specific optimizations
    - Custom PostgreSQL query hints

    For standard operations, the inherited implementation is sufficient.
    The __init__ is automatically inherited from the parent class.

    Attributes:
        session: SQLModel session for database operations (inherited).
    """

    # PostgreSQL-specific methods or overrides can be added here if needed
    # Most of the time, this class will be empty (just inheriting)
    pass


class AsyncPostgreSQLArchiveRepository(AsyncSQLArchiveRepository):
    """PostgreSQL implementation of Archive repository (asynchronous).

    Inherits all operations from AsyncSQLArchiveRepository. Override methods
    here only when PostgreSQL-specific functionality is needed, such as:
    - PostgreSQL-specific JSON operators
    - Full-text search
    - PostgreSQL-specific async optimizations
    - Custom PostgreSQL query hints

    For standard operations, the inherited implementation is sufficient.
    The __init__ is automatically inherited from the parent class.

    Attributes:
        session: Async SQLAlchemy session for database operations (inherited).
    """

    # PostgreSQL-specific methods or overrides can be added here if needed
    # Most of the time, this class will be empty (just inheriting)
    pass
