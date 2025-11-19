"""Assign restaurant owner by admin schemas.

This module contains schemas for assigning an owner to a restaurant by administrators.
Corresponds to: routes/restaurant/admin/assign_restaurant_owner_by_admin.py
"""

from pydantic import BaseModel, Field

from app.domains.restaurants.presentation.api.schemas.restaurant.common import (
    BaseOwnershipSchema,
)


class AssignRestaurantOwnerByAdminSchemaRequest(BaseModel):
    """Request schema for assigning an owner to a restaurant by admin.

    Attributes:
        owner_id: ULID of the user to assign as owner
        role: Role in restaurant management
        is_primary: Whether this is the primary owner
    """

    owner_id: str = Field(
        ...,
        min_length=26,
        max_length=26,
        description="ULID of the user to assign as owner",
        examples=["01HKJZW8X9ABCDEFGHIJK12345"],
    )

    role: str = Field(
        default="owner",
        max_length=50,
        description="Role in restaurant management (owner, manager, staff)",
        examples=["owner", "manager", "staff"],
    )

    is_primary: bool = Field(
        default=False,
        description="Whether this is the primary owner of the restaurant",
    )


class AssignRestaurantOwnerByAdminSchemaResponse(BaseOwnershipSchema):
    """Response schema for assign restaurant owner by admin endpoint.

    Inherits all fields from BaseOwnershipSchema.
    This is the admin-specific response for ownership assignment operations.

    Example:
        {
            "restaurant_id": "01HKJZW8X9ABCDEFGHIJK12345",
            "owner_id": "01HKJZW8Y9ABCDEFGHIJK12345",
            "role": "owner",
            "is_primary": true,
            "created_at": "2025-11-19T10:30:00Z",
            "updated_at": "2025-11-19T10:30:00Z",
            "created_by": "01HKJZW8Z9ABCDEFGHIJK12345",
            "updated_by": null
        }
    """

    pass


__all__ = [
    "AssignRestaurantOwnerByAdminSchemaRequest",
    "AssignRestaurantOwnerByAdminSchemaResponse",
]
