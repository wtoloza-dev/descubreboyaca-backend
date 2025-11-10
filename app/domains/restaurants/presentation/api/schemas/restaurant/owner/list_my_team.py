"""List my team schemas.

This module contains schemas for listing team members of a restaurant.
Corresponds to: routes/restaurant/owner/list_my_team.py
"""

from pydantic import BaseModel, Field

from app.domains.restaurants.presentation.api.schemas.restaurant.common import (
    OwnershipSchemaResponse,
)


class ListMyTeamSchemaResponse(BaseModel):
    """Response schema for listing restaurant team members.

    Attributes:
        restaurant_id: Restaurant ULID
        team_members: List of team members (ownership records)
        total: Total number of team members
    """

    restaurant_id: str = Field(description="Restaurant ULID")
    team_members: list[OwnershipSchemaResponse] = Field(
        description="List of team members"
    )
    total: int = Field(description="Total number of team members")


__all__ = ["ListMyTeamSchemaResponse"]
