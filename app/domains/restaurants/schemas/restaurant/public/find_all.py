"""Restaurant schemas for find all endpoint.

This module defines schemas for finding all restaurants with pagination.
Corresponds to: routes/restaurant/public/find_all.py
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain import GeoLocation
from app.shared.schemas import PaginatedResponse


class ListRestaurantsSchemaItem(BaseModel):
    """Restaurant item in list restaurants response.

    Includes essential information without full details to optimize
    response size for list operations.

    Attributes:
        id: Unique identifier (ULID)
        name: Restaurant name
        description: Restaurant description
        city: City or municipality
        state: State or department
        location: GPS coordinates
        phone: Contact phone number
        establishment_types: Types of establishment
        cuisine_types: Types of cuisine
        price_level: Price level (1-4)
        features: List of features/amenities
        tags: List of tags
        created_at: Creation timestamp
        updated_at: Last update timestamp

    Example:
        {
            "id": "01HQZX123456789ABCDEFGHIJK",
            "name": "La Casona Boyacense",
            "city": "Tunja",
            "cuisine_types": ["Boyacense", "Colombiana"],
            "price_level": 2,
            "location": {
                "latitude": 5.5353,
                "longitude": -73.3678
            }
        }
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

    # Business classification and categorization
    establishment_types: list[str] = Field(
        default_factory=list, description="Types of establishment"
    )
    cuisine_types: list[str] = Field(
        default_factory=list, description="Types of cuisine"
    )
    price_level: int | None = Field(None, description="Price level (1-4)")
    features: list[str] = Field(default_factory=list, description="Features/amenities")
    tags: list[str] = Field(default_factory=list, description="Tags")

    # Timestamps (useful for sorting)
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")


class ListRestaurantsSchemaResponse(PaginatedResponse[ListRestaurantsSchemaItem]):
    """Paginated response for list restaurants endpoint.

    Attributes:
        items: List of restaurants
        page: Current page number
        page_size: Number of items per page
        total: Total number of restaurants

    Example:
        {
            "items": [
                {
                    "id": "01HQZX123456789ABCDEFGHIJK",
                    "name": "La Casona Boyacense",
                    "city": "Tunja",
                    ...
                }
            ],
            "page": 1,
            "page_size": 20,
            "total": 42
        }
    """

    pass
