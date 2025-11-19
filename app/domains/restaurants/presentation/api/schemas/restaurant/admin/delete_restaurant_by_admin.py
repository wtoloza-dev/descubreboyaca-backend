"""Delete restaurant by admin schemas.

This module defines request/response schemas for restaurant deletion operations by administrators.
Corresponds to: routes/restaurant/admin/delete_restaurant_by_admin.py
"""

from pydantic import BaseModel, Field


class DeleteRestaurantByAdminSchemaRequest(BaseModel):
    """Request schema for deleting a restaurant by admin.

    Attributes:
        note: Optional explanation for the deletion (for audit trail)

    Example:
        >>> DeleteRestaurantByAdminSchemaRequest(note="Permanently closed")
    """

    note: str | None = Field(
        default=None,
        max_length=500,
        description="Optional note explaining the reason for deletion (stored in archive)",
        examples=["Restaurant permanently closed", "Duplicate entry", "Owner request"],
    )
