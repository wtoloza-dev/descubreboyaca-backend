"""List dish reviews schema.

This module defines the schema for listing reviews of a specific dish.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import PaginationSchemaData, PaginationSchemaResponse


class ListDishReviewsSchemaItem(BaseModel):
    """List dish reviews schema item.

    This schema is used to represent a review in the public list.
    Only approved reviews should be returned by public endpoints.

    Attributes:
        id: Unique identifier of the review
        user_id: ULID of the user who created the review
        rating: Rating from 1 to 5 stars
        title: Optional review title/summary
        comment: Optional detailed review text
        photos: List of photo URLs
        visit_date: Optional date when the user visited
        created_at: Timestamp when the review was created
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Unique identifier (ULID)")
    user_id: str = Field(description="User ULID who created the review")
    rating: int = Field(ge=1, le=5, description="Rating from 1 to 5 stars")
    title: str | None = Field(default=None, description="Review title/summary")
    comment: str | None = Field(default=None, description="Review comment/text")
    photos: list[str] = Field(default_factory=list, description="List of photo URLs")
    visit_date: datetime | None = Field(
        default=None,
        description="Date when the user visited",
    )
    created_at: datetime = Field(description="Review creation timestamp")


class ListDishReviewsSchemaResponse(
    PaginationSchemaResponse[ListDishReviewsSchemaItem]
):
    """List dish reviews schema response.

    This schema is used to list dish reviews with pagination.

    Attributes:
        data: List of approved reviews
        pagination: Pagination metadata
    """

    data: list[ListDishReviewsSchemaItem] = Field(description="List of dish reviews")
    pagination: PaginationSchemaData = Field(description="Pagination metadata")
