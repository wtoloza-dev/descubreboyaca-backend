"""Favorites domain exceptions."""

from app.domains.favorites.domain.exceptions.favorite_exceptions import (
    FavoriteAlreadyExistsError,
    FavoriteNotFoundError,
)


__all__ = [
    "FavoriteAlreadyExistsError",
    "FavoriteNotFoundError",
]
