"""Favorites API schemas."""

from app.domains.favorites.schemas.add import (
    AddFavoriteRequest,
    AddFavoriteResponse,
)
from app.domains.favorites.schemas.check import CheckFavoriteResponse
from app.domains.favorites.schemas.favorite import FavoriteResponse
from app.domains.favorites.schemas.list import ListFavoritesResponse


__all__ = [
    "AddFavoriteRequest",
    "AddFavoriteResponse",
    "CheckFavoriteResponse",
    "FavoriteResponse",
    "ListFavoritesResponse",
]
