"""Update owner role schemas.

This module contains request and response schemas for updating an owner's role.
Corresponds to: routes/restaurant/admin/update_owner_role.py
"""

from pydantic import BaseModel, Field

from app.domains.restaurants.schemas.restaurant.common import OwnershipSchemaResponse


class UpdateOwnerRoleSchemaRequest(BaseModel):
    """Request schema for updating an owner's role.

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


# Response is OwnershipSchemaResponse from common
__all__ = ["UpdateOwnerRoleSchemaRequest", "OwnershipSchemaResponse"]
