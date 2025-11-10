"""Favorites repositories."""

from .favorite import (
    PostgreSQLFavoriteRepository,
    SQLiteFavoriteRepository,
)


__all__ = [
    "SQLiteFavoriteRepository",
    "PostgreSQLFavoriteRepository",
]
