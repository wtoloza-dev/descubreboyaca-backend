"""List my reviews schema.

This module defines the schema for listing my reviews.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import PaginationSchemaData, PaginationSchemaResponse


class ListMyReviewsSchemaItem(BaseModel):
    """List my reviews schema item.

    This schema is used to represent a review in the list.

    Attributes:
        id: Unique identifier of the review
    """

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(description="Unique identifier (ULID)")


class ListMyReviewsSchemaResponse(PaginationSchemaResponse[ListMyReviewsSchemaItem]):
    """List my reviews schema response.

    This schema is used to list my reviews with pagination.

    Attributes:
        data: List of reviews
        pagination: Pagination metadata
    """

    data: list[ListMyReviewsSchemaItem] = Field(description="List of reviews")
    pagination: PaginationSchemaData = Field(description="Pagination metadata")
