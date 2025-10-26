"""Delete restaurant schemas.

This module defines request/response schemas for restaurant deletion operations.
"""

from pydantic import BaseModel, Field


class DeleteRestaurantSchemaRequest(BaseModel):
    """Request schema for deleting a restaurant.

    Attributes:
        note: Optional explanation for the deletion (for audit trail)

    Example:
        >>> DeleteRestaurantRequest(note="Permanently closed")
    """

    note: str | None = Field(
        default=None,
        max_length=500,
        description="Optional note explaining the reason for deletion (stored in archive)",
        examples=["Restaurant permanently closed", "Duplicate entry", "Owner request"],
    )
