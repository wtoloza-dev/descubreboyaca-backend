"""Common ownership schemas - BASE CLASSES ONLY.

This module contains BASE schemas for ownership operations.
These are meant to be INHERITED by layer-specific schemas, NOT used directly.

WARNING: Do not import these directly in routes or other modules.
         Each layer (admin, owner, public) should define its own schemas
         that inherit from these base classes.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseOwnershipSchema(BaseModel):
    """Base schema for restaurant ownership information.

    This is a BASE class meant to be inherited by layer-specific schemas.
    Do NOT use this directly in routes or endpoints.

    Attributes:
        restaurant_id: Restaurant ULID
        owner_id: Owner/user ULID
        role: Role in restaurant
        is_primary: Whether primary owner
        created_at: Creation timestamp
        updated_at: Last update timestamp
        created_by: Creator user ID
        updated_by: Last updater user ID
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
