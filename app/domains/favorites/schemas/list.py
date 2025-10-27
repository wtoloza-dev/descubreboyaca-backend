"""List favorites schemas.

This module defines response schemas for listing favorites.
"""

from app.domains.favorites.schemas.favorite import FavoriteResponse
from app.shared.schemas.pagination import PaginatedResponse


class ListFavoritesResponse(PaginatedResponse[FavoriteResponse]):
    """Response schema for listing favorites.

    Inherits pagination fields from PaginatedResponse and uses
    FavoriteResponse as the item type.

    Attributes:
        items: List of favorites
        page: Current page number
        page_size: Number of items per page
        total: Total number of favorites
    """

    pass
