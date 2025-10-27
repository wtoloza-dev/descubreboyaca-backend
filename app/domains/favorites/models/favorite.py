"""Favorite database model.

This module defines the Favorite ORM model for database operations.
"""

from datetime import datetime

from sqlalchemy import Column, ForeignKey, Index, String, UniqueConstraint
from sqlmodel import Field, SQLModel


class FavoriteModel(SQLModel, table=True):
    """Favorite database model.

    This model represents a polymorphic favorites table that can store
    favorites for any type of entity (restaurants, dishes, events, etc.).

    The design is scalable - adding new entity types only requires updating
    the EntityType enum, no schema changes needed.

    Attributes:
        id: ULID primary key (must be provided by domain entity)
        user_id: Foreign key to users table
        entity_type: Type of entity (restaurant, dish, event, place, activity)
        entity_id: ULID of the favorited entity
        created_at: Timestamp when favorite was created (must be provided)
    """

    __tablename__ = "favorites"

    # Primary key
    id: str = Field(primary_key=True, max_length=26)

    # Foreign key to users
    user_id: str = Field(
        sa_column=Column(
            String(26),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        description="User who created the favorite",
    )

    # Polymorphic fields
    entity_type: str = Field(max_length=50, nullable=False, index=True)
    entity_id: str = Field(max_length=26, nullable=False, index=True)

    # Timestamp
    created_at: datetime = Field(nullable=False, index=True)

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
