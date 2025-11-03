"""Favorite repository implementations.

This package contains different database implementations for the favorite repository.
"""

from .postgresql import PostgreSQLFavoriteRepository
from .sqlite import SQLiteFavoriteRepository


__all__ = [
    "SQLiteFavoriteRepository",
    "PostgreSQLFavoriteRepository",
]
