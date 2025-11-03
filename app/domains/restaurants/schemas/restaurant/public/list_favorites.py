"""List favorite restaurants schemas.

This module contains schemas for listing user's favorite restaurants.
Corresponds to: routes/restaurant/public/list_favorites.py
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain import GeoLocation
from app.shared.schemas import PaginatedResponse


class ListFavoriteRestaurantsSchemaItem(BaseModel):
    """Restaurant item in favorites list response.

    Includes essential information optimized for favorites views.
    """

    model_config = ConfigDict(from_attributes=True)

    # Identity
    id: str = Field(description="Unique identifier (ULID)")

    # Basic information
    name: str = Field(description="Restaurant name")
    description: str | None = Field(None, description="Restaurant description")

    # Location
    city: str = Field(description="City or municipality")
    state: str = Field(description="State or department")
    location: GeoLocation | None = Field(None, description="GPS coordinates")

    # Contact
    phone: str = Field(description="Contact phone number")

    # Classification
    establishment_types: list[str] = Field(
        default_factory=list, description="Types of establishment"
    )
    cuisine_types: list[str] = Field(
        default_factory=list, description="Types of cuisine"
    )
    price_level: int | None = Field(None, description="Price level (1-4)")

    # Additional
    features: list[str] = Field(default_factory=list, description="Features/amenities")
    tags: list[str] = Field(default_factory=list, description="Tags")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class ListFavoriteRestaurantsSchemaResponse(
    PaginatedResponse[ListFavoriteRestaurantsSchemaItem]
):
    """Paginated response for favorite restaurants.

    Attributes:
        items: List of favorite restaurants
        page: Current page number
        page_size: Number of items per page
        total: Total number of favorites
    """

    items: list[ListFavoriteRestaurantsSchemaItem] = Field(
        description="List of favorite restaurants"
    )
    page: int = Field(description="Current page")
    page_size: int = Field(description="Items per page")
    total: int = Field(description="Total count")


__all__ = ["ListFavoriteRestaurantsSchemaItem", "ListFavoriteRestaurantsSchemaResponse"]
