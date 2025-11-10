"""Restaurant owner repository implementations.

This package contains SQLite and PostgreSQL implementations for restaurant owner persistence.
"""

from .postgresql import PostgreSQLRestaurantOwnerRepository
from .sqlite import SQLiteRestaurantOwnerRepository


__all__ = [
    "SQLiteRestaurantOwnerRepository",
    "PostgreSQLRestaurantOwnerRepository",
]
