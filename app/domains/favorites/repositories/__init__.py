"""Favorites repositories."""

from app.domains.favorites.repositories.favorite import (
    PostgreSQLFavoriteRepository,
    SQLiteFavoriteRepository,
)


__all__ = [
    "SQLiteFavoriteRepository",
    "PostgreSQLFavoriteRepository",
]
