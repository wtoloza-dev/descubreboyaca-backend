"""Favorite SQLite implementation.

This module provides the SQLite repository implementation for Favorite persistence operations.
SQLite implementation inherits from the common SQL repository.
"""

from .common import SQLFavoriteRepository


class SQLiteFavoriteRepository(SQLFavoriteRepository):
    """Favorite SQLite implementation using async operations.

    This repository inherits all CRUD operations from SQLFavoriteRepository.
    Override methods here only when SQLite-specific functionality is needed:
    - SQLite-specific optimizations
    - SQLite-specific query syntax
    - SQLite-specific features

    For standard CRUD operations, the inherited implementation is sufficient.
    The __init__ is automatically inherited from the parent class.

    Attributes:
        session: SQLModel async session for database operations (inherited).
    """

    # SQLite-specific methods or overrides can be added here if needed
    # Most of the time, this class will be empty (just inheriting)
    pass
