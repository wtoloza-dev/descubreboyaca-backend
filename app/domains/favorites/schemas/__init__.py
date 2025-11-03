"""Favorites API schemas."""

from app.domains.favorites.schemas.add import (
    AddFavoriteSchemaRequest,
    AddFavoriteSchemaResponse,
)
from app.domains.favorites.schemas.check import CheckFavoriteSchemaResponse
from app.domains.favorites.schemas.favorite import FavoriteSchemaResponse
from app.domains.favorites.schemas.list import ListFavoritesSchemaResponse


__all__ = [
    "AddFavoriteSchemaRequest",
    "AddFavoriteSchemaResponse",
    "CheckFavoriteSchemaResponse",
    "FavoriteSchemaResponse",
    "ListFavoritesSchemaResponse",
]
