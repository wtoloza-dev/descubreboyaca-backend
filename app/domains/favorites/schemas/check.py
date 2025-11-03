"""Check favorite schemas.

This module defines response schema for checking if entity is favorited.
Corresponds to: routes/check.py
"""

from pydantic import BaseModel, Field


class CheckFavoriteSchemaResponse(BaseModel):
    """Response schema for checking if entity is favorited.

    Attributes:
        is_favorite: Whether the entity is favorited by the user
        favorite_id: ULID of the favorite if it exists, None otherwise
    """

    is_favorite: bool = Field(description="Whether entity is favorited")
    favorite_id: str | None = Field(
        default=None, description="Favorite ULID if favorited, None otherwise"
    )
