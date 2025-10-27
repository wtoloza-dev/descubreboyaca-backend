"""Favorite base schema.

This module defines the base favorite response schema.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domains.favorites.domain.enums import EntityType


class FavoriteResponse(BaseModel):
    """Response schema for a favorite.

    This schema represents a favorite in API responses.

    Attributes:
        id: Favorite ULID
        user_id: User ULID
        entity_type: Type of favorited entity
        entity_id: Entity ULID
        created_at: Timestamp when favorite was created
    """

    id: str = Field(description="Favorite ULID")
    user_id: str = Field(description="User ULID")
    entity_type: EntityType = Field(description="Type of favorited entity")
    entity_id: str = Field(description="Entity ULID")
    created_at: datetime = Field(description="Creation timestamp")

    # Enable validation from ORM/domain entities
    model_config = ConfigDict(from_attributes=True)
