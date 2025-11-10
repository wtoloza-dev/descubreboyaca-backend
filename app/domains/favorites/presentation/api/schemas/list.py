"""List favorites schemas.

This module defines response schemas for listing favorites.
Corresponds to: routes/list.py
"""

from pydantic import Field

from app.domains.favorites.presentation.api.schemas.favorite import (
    FavoriteSchemaResponse,
)
from app.shared.schemas.pagination import PaginationSchemaData, PaginationSchemaResponse


class ListFavoritesSchemaResponse(PaginationSchemaResponse[FavoriteSchemaResponse]):
    """Response schema for listing favorites.

    Inherits pagination structure from PaginationSchemaResponse and uses
    FavoriteSchemaResponse as the item type.

    Attributes:
        data: List of favorites
        pagination: Pagination metadata
    """

    data: list[FavoriteSchemaResponse] = Field(description="List of favorites")
    pagination: PaginationSchemaData = Field(description="Pagination metadata")
