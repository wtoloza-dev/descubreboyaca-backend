"""List restaurants by city schemas.

This module contains schemas for listing restaurants filtered by city.
Corresponds to: routes/restaurant/public/list_by_city.py
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain import GeoLocation
from app.shared.schemas import PaginatedResponse


class ListRestaurantsByCitySchemaItem(BaseModel):
    """Restaurant item in list by city response.

    Includes essential information optimized for list views.
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


class ListRestaurantsByCitySchemaResponse(
    PaginatedResponse[ListRestaurantsByCitySchemaItem]
):
    """Paginated response for restaurants by city.

    Attributes:
        items: List of restaurants in the city
        page: Current page number
        page_size: Number of items per page
        total: Total number of restaurants
    """

    items: list[ListRestaurantsByCitySchemaItem] = Field(
        description="List of restaurants"
    )
    page: int = Field(description="Current page")
    page_size: int = Field(description="Items per page")
    total: int = Field(description="Total count")


__all__ = ["ListRestaurantsByCitySchemaItem", "ListRestaurantsByCitySchemaResponse"]
