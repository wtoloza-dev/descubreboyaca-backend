"""Find my team schemas.

This module contains schemas for finding team members of a restaurant.
Corresponds to: routes/restaurant/owner/find_my_team.py
"""

from pydantic import BaseModel, ConfigDict, Field


class FindMyTeamSchemaItem(BaseModel):
    """Team member item in team list response.

    Attributes:
        owner_id: Owner/manager user ULID
        role: Role in restaurant management
        is_primary: Whether this is the primary owner

    Example:
        {
            "owner_id": "01HKJZW8X9ABCDEFGHIJK12345",
            "role": "owner",
            "is_primary": true
        }
    """

    owner_id: str = Field(description="Owner/manager user ULID")
    role: str = Field(description="Role in restaurant management")
    is_primary: bool = Field(description="Whether this is the primary owner")

    model_config = ConfigDict(from_attributes=True)


class FindMyTeamSchemaResponse(BaseModel):
    """Response schema for finding restaurant team members.

    Attributes:
        restaurant_id: Restaurant ULID
        team: List of team members
        total: Total number of team members

    Example:
        {
            "restaurant_id": "01HKJZW8X9ABCDEFGHIJK12345",
            "team": [
                {
                    "owner_id": "01HKJZW8X...",
                    "role": "owner",
                    "is_primary": true
                },
                {
                    "owner_id": "01HKJZW9Y...",
                    "role": "manager",
                    "is_primary": false
                }
            ],
            "total": 2
        }
    """

    restaurant_id: str = Field(description="Restaurant ULID")
    team: list[FindMyTeamSchemaItem] = Field(description="List of team members")
    total: int = Field(description="Total number of team members")


__all__ = ["FindMyTeamSchemaItem", "FindMyTeamSchemaResponse"]
