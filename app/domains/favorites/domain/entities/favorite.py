"""Favorite domain entities following DDD principles.

This module defines the core favorite entity used in the domain layer.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.domains.favorites.domain.enums import EntityType
from app.shared.domain.entities import AuditBasic


class FavoriteData(BaseModel):
    """Favorite data without ID and timestamps.

    This class represents the essential data needed to create a favorite,
    without the auto-generated fields (id, created_at).

    Attributes:
        user_id: ULID of the user who created the favorite
        entity_type: Type of entity being favorited
        entity_id: ULID of the entity being favorited
    """

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    user_id: str = Field(max_length=26, description="User ULID")
    entity_type: EntityType = Field(description="Type of entity being favorited")
    entity_id: str = Field(max_length=26, description="Entity ULID")


class Favorite(FavoriteData, AuditBasic):
    """Complete favorite entity with auto-generated fields.

    This class extends FavoriteData with id and timestamp fields that are
    automatically generated when a favorite is created.

    Following DDD principles, the entity generates its own identity (ULID)
    and audit fields through inheritance from AuditBasic.

    Attributes:
        id: Auto-generated ULID (inherited from AuditBasic)
        created_at: Auto-generated UTC timestamp (inherited from AuditBasic)
        updated_at: Auto-generated UTC timestamp of last update (inherited from AuditBasic)
        user_id: ULID of the user who created the favorite
        entity_type: Type of entity being favorited
        entity_id: ULID of the entity being favorited
    """
