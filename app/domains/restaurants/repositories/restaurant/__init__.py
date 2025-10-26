"""Restaurant repository implementations.

This package contains SQLite and PostgreSQL implementations for restaurant persistence.
"""

from .postgresql import RestaurantRepositoryPostgreSQL
from .sqlite import RestaurantRepositorySQLite


__all__ = [
    "RestaurantRepositorySQLite",
    "RestaurantRepositoryPostgreSQL",
]
