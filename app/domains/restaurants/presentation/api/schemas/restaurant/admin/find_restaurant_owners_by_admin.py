"""Find restaurant owners by admin schemas.

This module contains schemas for finding restaurant owners by administrators.
Corresponds to: routes/restaurant/admin/find_restaurant_owners_by_admin.py
"""

from pydantic import BaseModel, Field

from app.domains.restaurants.presentation.api.schemas.restaurant.common import (
    BaseOwnershipSchema,
)


class FindRestaurantOwnersByAdminSchemaItem(BaseOwnershipSchema):
    """Individual ownership item in the admin find owners response.

    Inherits all fields from BaseOwnershipSchema.
    This represents a single ownership relationship in the list.
    """

    pass


class FindRestaurantOwnersByAdminSchemaResponse(BaseModel):
    """Response schema for finding restaurant owners by admin.

    Attributes:
        restaurant_id: Restaurant ULID
        owners: List of ownership records
        total: Total number of owners

    Example:
        {
            "restaurant_id": "01HKJZW8X9ABCDEFGHIJK12345",
            "owners": [
                {
                    "restaurant_id": "01HKJZW8X...",
                    "owner_id": "01HKJZW8Y...",
                    "role": "owner",
                    "is_primary": true,
                    ...
                },
                {
                    "restaurant_id": "01HKJZW8X...",
                    "owner_id": "01HKJZW8Z...",
                    "role": "manager",
                    "is_primary": false,
                    ...
                }
            ],
            "total": 2
        }
    """

    restaurant_id: str = Field(description="Restaurant ULID")
    owners: list[FindRestaurantOwnersByAdminSchemaItem] = Field(
        description="List of ownership records"
    )
    total: int = Field(description="Total number of owners")


__all__ = [
    "FindRestaurantOwnersByAdminSchemaItem",
    "FindRestaurantOwnersByAdminSchemaResponse",
]
