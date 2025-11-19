"""Transfer restaurant ownership by admin schemas.

This module contains response schemas for transferring restaurant ownership by administrators.
Corresponds to: routes/restaurant/admin/transfer_restaurant_ownership_by_admin.py
"""

from app.domains.restaurants.presentation.api.schemas.restaurant.common import (
    BaseOwnershipSchema,
)


class TransferRestaurantOwnershipByAdminSchemaResponse(BaseOwnershipSchema):
    """Response schema for transfer restaurant ownership by admin endpoint.

    Inherits all fields from BaseOwnershipSchema.
    This is the admin-specific response for ownership transfer operations.

    Example:
        {
            "restaurant_id": "01HKJZW8X9ABCDEFGHIJK12345",
            "owner_id": "01HKJZW8Y9ABCDEFGHIJK12345",
            "role": "owner",
            "is_primary": true,
            "created_at": "2025-11-19T10:30:00Z",
            "updated_at": "2025-11-19T11:30:00Z",
            "created_by": "01HKJZW8Z9ABCDEFGHIJK12345",
            "updated_by": "01HKJZW8A9ABCDEFGHIJK12345"
        }
    """

    pass


__all__ = ["TransferRestaurantOwnershipByAdminSchemaResponse"]
