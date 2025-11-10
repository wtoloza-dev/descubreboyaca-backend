"""Favorites API schemas."""

from app.domains.favorites.presentation.api.schemas.add import (
    AddFavoriteSchemaRequest,
    AddFavoriteSchemaResponse,
)
from app.domains.favorites.presentation.api.schemas.check import (
    CheckFavoriteSchemaResponse,
)
from app.domains.favorites.presentation.api.schemas.favorite import (
    FavoriteSchemaResponse,
)
from app.domains.favorites.presentation.api.schemas.list import (
    ListFavoritesSchemaResponse,
)


__all__ = [
    "AddFavoriteSchemaRequest",
    "AddFavoriteSchemaResponse",
    "CheckFavoriteSchemaResponse",
    "FavoriteSchemaResponse",
    "ListFavoritesSchemaResponse",
]
