"""Restaurant schemas for list endpoint.

This module defines schemas for listing restaurants with pagination.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.shared.domain import GeoLocation
from app.shared.schemas import PaginatedResponse


class RestaurantSchemaListItem(BaseModel):
    """Restaurant representation for list views.

    Includes essential information without full details to optimize
    response size for list operations.

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

    # Identity
    id: str

    # Basic information
    name: str
    description: str | None

    # Location
    city: str
    state: str
    location: GeoLocation | None

    # Contact
    phone: str

    # Business classification and categorization
    establishment_types: list[str]
    cuisine_types: list[str]
    price_level: int | None
    features: list[str]
    tags: list[str]

    # Timestamps (useful for sorting)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ListRestaurantsSchemaResponse(PaginatedResponse[RestaurantSchemaListItem]):
    """Paginated response for list restaurants endpoint.

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
