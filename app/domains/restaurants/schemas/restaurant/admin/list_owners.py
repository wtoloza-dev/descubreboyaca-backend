"""List owners schemas.

This module contains schemas for listing restaurant owners.
Corresponds to: routes/restaurant/admin/list_owners.py
"""

from pydantic import BaseModel, Field

from app.domains.restaurants.schemas.restaurant.common import OwnershipSchemaResponse


class ListOwnershipsSchemaResponse(BaseModel):
    """Response schema for listing restaurant owners.

    Attributes:
        restaurant_id: Restaurant ULID
        owners: List of ownership records
        total: Total number of owners
    """

    restaurant_id: str = Field(description="Restaurant ULID")
    owners: list[OwnershipSchemaResponse] = Field(
        description="List of ownership records"
    )
    total: int = Field(description="Total number of owners")


__all__ = ["ListOwnershipsSchemaResponse"]
