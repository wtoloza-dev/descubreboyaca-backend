"""Update restaurant owner role by admin schemas.

This module contains request and response schemas for updating an owner's role by administrators.
Corresponds to: routes/restaurant/admin/update_restaurant_owner_role_by_admin.py
"""

from pydantic import BaseModel, Field

from app.domains.restaurants.presentation.api.schemas.restaurant.common import (
    BaseOwnershipSchema,
)


class UpdateRestaurantOwnerRoleByAdminSchemaRequest(BaseModel):
    """Request schema for updating an owner's role by admin.

    Attributes:
        role: New role for the owner

    Example:
        {
            "role": "manager"
        }
    """

    role: str = Field(
        ...,
        max_length=50,
        description="New role (owner, manager, staff)",
        examples=["owner", "manager", "staff"],
    )


class UpdateRestaurantOwnerRoleByAdminSchemaResponse(BaseOwnershipSchema):
    """Response schema for update restaurant owner role by admin endpoint.

    Inherits all fields from BaseOwnershipSchema.
    This is the admin-specific response for role update operations.

    Example:
        {
            "restaurant_id": "01HKJZW8X9ABCDEFGHIJK12345",
            "owner_id": "01HKJZW8Y9ABCDEFGHIJK12345",
            "role": "manager",
            "is_primary": false,
            "created_at": "2025-11-19T10:30:00Z",
            "updated_at": "2025-11-19T11:00:00Z",
            "created_by": "01HKJZW8Z9ABCDEFGHIJK12345",
            "updated_by": "01HKJZW8Z9ABCDEFGHIJK12345"
        }
    """

    pass


__all__ = [
    "UpdateRestaurantOwnerRoleByAdminSchemaRequest",
    "UpdateRestaurantOwnerRoleByAdminSchemaResponse",
]
