"""Find owners schemas.

This module contains schemas for finding restaurant owners.
Corresponds to: routes/restaurant/admin/find_owners.py
"""

from pydantic import BaseModel, Field

from app.domains.restaurants.presentation.api.schemas.restaurant.common import (
    OwnershipSchemaResponse,
)


class FindOwnershipsSchemaResponse(BaseModel):
    """Response schema for finding restaurant owners.

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


__all__ = ["FindOwnershipsSchemaResponse"]
