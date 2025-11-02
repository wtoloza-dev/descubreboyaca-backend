"""List my reviews schema.

This module defines the schema for listing my reviews.
"""

from pydantic import BaseModel

from app.shared.schemas import PaginatedResponse


class ListMyReviewsSchemaItem(BaseModel):
    """List my reviews schema item.

    This schema is used to represent a review.
    """

    id: str


class ListMyReviewsSchemaResponse(PaginatedResponse[ListMyReviewsSchemaItem]):
    """List my reviews schema.

    This schema is used to list my reviews.
    """
