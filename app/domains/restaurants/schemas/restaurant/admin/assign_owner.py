"""Assign owner schemas.

This module contains schemas for assigning an owner to a restaurant.
Corresponds to: routes/restaurant/admin/assign_owner.py
"""

from pydantic import BaseModel, Field

from app.domains.restaurants.schemas.restaurant.common import OwnershipSchemaResponse


class AssignOwnerSchemaRequest(BaseModel):
    """Request schema for assigning an owner to a restaurant.

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


# Response is OwnershipSchemaResponse from common
__all__ = ["AssignOwnerSchemaRequest", "OwnershipSchemaResponse"]
