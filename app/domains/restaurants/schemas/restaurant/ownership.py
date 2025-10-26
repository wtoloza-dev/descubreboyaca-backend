"""Restaurant ownership schemas.

This module defines schemas for managing restaurant ownership relationships.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssignOwnerSchemaRequest(BaseModel):
    """Request schema for assigning an owner to a restaurant.

    Example:
        {
            "owner_id": "01HKJZW8X...",
            "role": "owner",
            "is_primary": true
        }
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


class UpdateOwnerRoleSchemaRequest(BaseModel):
    """Request schema for updating an owner's role.

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


class OwnershipSchemaResponse(BaseModel):
    """Response schema for restaurant ownership information.

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

    restaurant_id: str
    owner_id: str
    role: str
    is_primary: bool
    created_at: datetime
    updated_at: datetime
    created_by: str | None
    updated_by: str | None

    model_config = ConfigDict(from_attributes=True)


class OwnershipListSchemaResponse(BaseModel):
    """Response schema for listing restaurant owners.

    Example:
        {
            "restaurant_id": "01HKJZW8X...",
            "owners": [
                {
                    "owner_id": "01HKJZW8Y...",
                    "role": "owner",
                    "is_primary": true,
                    "created_at": "2025-10-23T09:37:35Z"
                }
            ],
            "total": 1
        }
    """

    restaurant_id: str
    owners: list[OwnershipSchemaResponse]
    total: int


class MyRestaurantSchemaItem(BaseModel):
    """Schema for a restaurant item in owner's restaurant list.

    Example:
        {
            "restaurant_id": "01HKJZW8X...",
            "restaurant_name": "Mi Restaurante",
            "role": "owner",
            "is_primary": true
        }
    """

    restaurant_id: str
    restaurant_name: str
    role: str
    is_primary: bool
    city: str
    state: str


class MyRestaurantsSchemaResponse(BaseModel):
    """Response schema for owner's restaurant list.

    Example:
        {
            "items": [...],
            "total": 5
        }
    """

    items: list[MyRestaurantSchemaItem]
    total: int
