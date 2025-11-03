"""Common ownership schemas.

This module contains base schemas for ownership operations that are shared
across admin and owner routes.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OwnershipSchemaResponse(BaseModel):
    """Response schema for restaurant ownership information.

    This is a shared schema used across multiple ownership-related endpoints.

    Attributes:
        restaurant_id: Restaurant ULID
        owner_id: Owner/user ULID
        role: Role in restaurant
        is_primary: Whether primary owner
        created_at: Creation timestamp
        updated_at: Last update timestamp
        created_by: Creator user ID
        updated_by: Last updater user ID

    Example:
        {
            "restaurant_id": "01HKJZW8X...",
            "owner_id": "01HKJZW8Y...",
            "role": "owner",
            "is_primary": true,
            "created_at": "2025-10-23T09:37:35Z",
            "created_by": "01HKJZW8Z..."
        }
    """

    model_config = ConfigDict(from_attributes=True)

    restaurant_id: str = Field(description="Restaurant ULID")
    owner_id: str = Field(description="Owner/user ULID")
    role: str = Field(description="Role in restaurant")
    is_primary: bool = Field(description="Whether primary owner")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    created_by: str | None = Field(None, description="Creator user ID")
    updated_by: str | None = Field(None, description="Last updater user ID")
