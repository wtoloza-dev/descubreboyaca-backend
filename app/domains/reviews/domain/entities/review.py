"""Review domain entity.

This module defines the core review entity used in the domain layer.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.shared.domain import AuditBasic

from ..enums import EntityType, ReviewStatus


class ReviewData(BaseModel):
    """Review data without ID and timestamps.

    This class represents the essential data needed to create a review,
    without the auto-generated fields (id, created_at, updated_at).

    Following DDD principles, this is the pure business data that defines
    a review.

    Attributes:
        entity_type: Type of entity being reviewed (restaurant, event, place, etc.)
        entity_id: ULID of the entity being reviewed
        user_id: ULID of the user who created the review
        rating: Rating from 1 to 5 stars
        title: Optional title/summary of the review
        comment: Optional detailed comment/review text
        photos: List of photo URLs associated with the review
        visit_date: Optional date when the user visited the entity
        status: Moderation status of the review (pending, approved, rejected)
    """

    entity_type: EntityType = Field(description="Type of entity being reviewed")
    entity_id: str = Field(max_length=26, description="Entity ULID")
    user_id: str = Field(max_length=26, description="User ULID")
    rating: int = Field(ge=1, le=5, description="Rating from 1 to 5 stars")
    title: str | None = Field(
        default=None,
        max_length=255,
        description="Review title/summary",
    )
    comment: str | None = Field(default=None, description="Review comment/text")
    photos: list[str] = Field(
        default_factory=list,
        description="List of photo URLs",
    )
    visit_date: datetime | None = Field(
        default=None,
        description="Date when the user visited",
    )
    status: ReviewStatus = Field(
        default=ReviewStatus.APPROVED,
        description="Moderation status",
    )


class Review(AuditBasic, ReviewData):
    """Complete review entity with auto-generated fields.

    This class extends ReviewData with id and timestamp fields that are
    automatically generated when a review is created.

    Following DDD principles, the entity generates its own identity using
    the shared ULID factory.

    Attributes:
        id: Auto-generated ULID (inherited from AuditBasic)
        created_at: Auto-generated UTC timestamp of creation (inherited from AuditBasic)
        updated_at: Auto-generated UTC timestamp of last update (inherited from AuditBasic)
        entity_type: Type of entity being reviewed
        entity_id: ULID of the entity being reviewed
        user_id: ULID of the user who created the review
        rating: Rating from 1 to 5 stars
        title: Optional title/summary of the review
        comment: Optional detailed comment/review text
        photos: List of photo URLs associated with the review
        visit_date: Optional date when the user visited the entity
        status: Moderation status of the review
    """
