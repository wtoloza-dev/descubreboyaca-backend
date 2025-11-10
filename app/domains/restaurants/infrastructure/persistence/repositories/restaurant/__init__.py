"""Restaurant repository implementations.

This package contains SQLite and PostgreSQL implementations for restaurant persistence.
"""

from .postgresql import PostgreSQLRestaurantRepository
from .sqlite import SQLiteRestaurantRepository


__all__ = [
    "SQLiteRestaurantRepository",
    "PostgreSQLRestaurantRepository",
]
