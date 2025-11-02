"""Review database model.

This module defines the Review ORM model for database operations.
"""

from datetime import datetime

from sqlalchemy import JSON, Column, ForeignKey, Index, String
from sqlmodel import Field, SQLModel

from app.shared.models import AuditBasicMixin


class ReviewModel(AuditBasicMixin, SQLModel, table=True):
    """Review database model.

    This model represents a polymorphic reviews table that can store
    reviews for any type of entity (restaurants, events, places, etc.).

    The design is scalable - adding new entity types only requires updating
    the EntityType enum, no schema changes needed.

    Following DDD principles, the ID and timestamps must be provided
    by the Review domain entity. This model only persists the data.

    Attributes:
        id: ULID primary key (inherited from AuditBasicMixin)
        created_at: Timestamp when review was created (inherited from AuditBasicMixin)
        updated_at: Timestamp when review was last updated (inherited from AuditBasicMixin)
        entity_type: Type of entity being reviewed (restaurant, event, place, etc.)
        entity_id: ULID of the entity being reviewed
        user_id: Foreign key to users table
        rating: Rating from 1 to 5 stars
        title: Optional review title/summary
        comment: Optional detailed review text
        photos: List of photo URLs (stored as JSON array)
        visit_date: Optional date when the user visited
        status: Moderation status (pending, approved, rejected)
    """

    __tablename__ = "reviews"

    # Polymorphic fields
    entity_type: str = Field(max_length=50, nullable=False, index=True)
    entity_id: str = Field(max_length=26, nullable=False, index=True)

    # Foreign key to users
    user_id: str = Field(
        sa_column=Column(
            String(26),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        description="User who created the review",
    )

    # Rating and content
    rating: int = Field(
        nullable=False,
        index=True,
        description="Rating from 1 to 5 stars",
    )
    title: str | None = Field(
        default=None,
        max_length=255,
        description="Review title/summary",
    )
    comment: str | None = Field(
        default=None,
        description="Review text/comment",
    )

    # Photos (stored as JSON array)
    photos: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, server_default="[]"),
        description="Array of photo URLs",
    )

    # Visit date
    visit_date: datetime | None = Field(
        default=None,
        description="Date when the user visited",
    )

    # Moderation status
    status: str = Field(
        default="approved",
        max_length=20,
        nullable=False,
        index=True,
        description="Moderation status: pending, approved, rejected",
    )

    # TODO: Revisar si los índices deben estar solo en migraciones o también en modelo
    # Opción 1: Solo en migración (single source of truth, más control)
    # Opción 2: Modelo + Migración (auto-documentación, tests con create_all())
    # Opción 3: Híbrido (constraints críticos en modelo, performance solo en migración)
    __table_args__ = (
        # Unique index: one user cannot review the same entity twice
        # This enforces the business rule at database level
        Index(
            "uq_reviews_user_entity",
            "user_id",
            "entity_type",
            "entity_id",
            unique=True,
        ),
        # Compound indexes for efficient queries
        Index("ix_reviews_entity", "entity_type", "entity_id"),
        Index("ix_reviews_user_status", "user_id", "status"),
        Index("ix_reviews_entity_status", "entity_type", "entity_id", "status"),
        Index("ix_reviews_entity_rating", "entity_type", "entity_id", "rating"),
    )
