"""Add favorite schemas.

This module defines request and response schemas for adding favorites.
"""

from pydantic import BaseModel, Field

from app.domains.favorites.domain.enums import EntityType
from app.domains.favorites.schemas.favorite import FavoriteResponse


class AddFavoriteRequest(BaseModel):
    """Request schema for adding a favorite.

    Attributes:
        entity_type: Type of entity to favorite
        entity_id: ULID of entity to favorite
    """

    entity_type: EntityType = Field(description="Type of entity to favorite")
    entity_id: str = Field(max_length=26, description="Entity ULID")


class AddFavoriteResponse(FavoriteResponse):
    """Response schema for adding a favorite.

    Inherits all fields from FavoriteResponse.
    """

    pass
