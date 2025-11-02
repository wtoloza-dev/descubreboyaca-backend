"""Favorites domain exceptions."""

from app.domains.favorites.domain.exceptions.favorite_already_exists import (
    FavoriteAlreadyExistsException,
)
from app.domains.favorites.domain.exceptions.favorite_not_found import (
    FavoriteNotFoundException,
)


__all__ = [
    "FavoriteAlreadyExistsException",
    "FavoriteNotFoundException",
]
