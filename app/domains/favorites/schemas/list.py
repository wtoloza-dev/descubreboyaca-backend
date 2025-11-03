"""List favorites schemas.

This module defines response schemas for listing favorites.
Corresponds to: routes/list.py
"""

from app.domains.favorites.schemas.favorite import FavoriteSchemaResponse
from app.shared.schemas.pagination import PaginatedResponse


class ListFavoritesSchemaResponse(PaginatedResponse[FavoriteSchemaResponse]):
    """Response schema for listing favorites.

    Inherits pagination fields from PaginatedResponse and uses
    FavoriteSchemaResponse as the item type.

    Attributes:
        items: List of favorites
        page: Current page number
        page_size: Number of items per page
        total: Total number of favorites
    """

    pass
