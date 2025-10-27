"""Favorite domain entity.

This module defines the core favorite entity used in the domain layer.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domains.favorites.domain.enums import EntityType
from app.shared.domain.factories.datetime import generate_utc_now
from app.shared.domain.factories.ulid import generate_ulid


class FavoriteData(BaseModel):
    """Favorite data without ID and timestamps.

    This class represents the essential data needed to create a favorite,
    without the auto-generated fields (id, created_at).

    Attributes:
        user_id: ULID of the user who created the favorite
        entity_type: Type of entity being favorited
        entity_id: ULID of the entity being favorited
    """

    user_id: str = Field(max_length=26, description="User ULID")
    entity_type: EntityType = Field(description="Type of entity being favorited")
    entity_id: str = Field(max_length=26, description="Entity ULID")


class Favorite(FavoriteData):
    """Complete favorite entity with auto-generated fields.

    This class extends FavoriteData with id and created_at fields that are
    automatically generated when a favorite is created.

    Following DDD principles, the entity generates its own identity using
    the shared ULID factory.

    Attributes:
        id: Auto-generated ULID
        user_id: ULID of the user who created the favorite
        entity_type: Type of entity being favorited
        entity_id: ULID of the entity being favorited
        created_at: Auto-generated UTC timestamp
    """

    id: str = Field(default_factory=generate_ulid, max_length=26)
    created_at: datetime = Field(default_factory=generate_utc_now)
    # Enable validation directly from ORM objects
    model_config = ConfigDict(from_attributes=True)
