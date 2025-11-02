"""Favorite model for database persistence.

This module defines the Favorite ORM model for database operations.
"""

from sqlalchemy import Index, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.shared.models import AuditBasicMixin


class FavoriteModel(AuditBasicMixin, SQLModel, table=True):
    """Favorite model for database persistence.

    This model represents a polymorphic favorites table that can store
    favorites for any type of entity (restaurants, dishes, events, etc.).

    The design is scalable - adding new entity types only requires updating
    the EntityType enum, no schema changes needed.

    Note: Following DDD principles, the ID and timestamps must be provided
    by the Favorite domain entity. This model only persists the data.

    Attributes:
        id: ULID primary key - inherited from AuditBasicMixin
        user_id: Foreign key to users table
        entity_type: Type of entity (restaurant, dish, event, place, activity)
        entity_id: ULID of the favorited entity
        created_at: Timestamp when favorite was created - inherited from AuditBasicMixin
        updated_at: Timestamp when favorite was last updated - inherited from AuditBasicMixin
    """

    __tablename__ = "favorites"

    # Foreign key to users
    user_id: str = Field(
        foreign_key="users.id",
        max_length=26,
        index=True,
        description="User who created the favorite",
    )

    # Polymorphic fields
    entity_type: str = Field(
        max_length=50,
        index=True,
        description="Type of entity being favorited",
    )
    entity_id: str = Field(
        max_length=26,
        index=True,
        description="ULID of the favorited entity",
    )

    __table_args__ = (
        # Unique constraint: one user cannot favorite the same entity twice
        UniqueConstraint(
            "user_id",
            "entity_type",
            "entity_id",
            name="uq_favorites_user_entity",
        ),
        # Compound index for efficient queries by user and type
        Index("ix_favorites_user_type", "user_id", "entity_type"),
        # Compound index for counting favorites on an entity
        Index("ix_favorites_entity", "entity_type", "entity_id"),
    )
