"""Restaurant schemas for get endpoint.

This module defines schemas for retrieving a single restaurant.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.shared.domain import GeoLocation, SocialMedia


class GetRestaurantSchemaResponse(BaseModel):
    """Response schema for get restaurant endpoint.

    Returns complete information about a single restaurant.

    Example:
        {
            "id": "01HQZX123456789ABCDEFGHIJK",
            "name": "La Casona Boyacense",
            "description": "Restaurante típico de comida boyacense",
            "address": "Calle 20 #10-52",
            "city": "Tunja",
            "state": "Boyacá",
            "country": "Colombia",
            "phone": "+573001234567",
            "location": {
                "latitude": 5.5353,
                "longitude": -73.3678
            },
            "cuisine_types": ["Boyacense", "Colombiana"],
            "price_level": 2,
            "created_at": "2025-10-21T10:30:00Z"
        }
    """

    # Identity
    id: str

    # Basic information
    name: str
    description: str | None

    # Address
    address: str
    city: str
    state: str
    postal_code: str | None
    country: str

    # Contact
    phone: str
    email: str | None
    website: str | None

    # Geolocation
    location: GeoLocation | None

    # Social media
    social_media: SocialMedia | None

    # Business classification and categorization
    establishment_types: list[str]
    cuisine_types: list[str]
    price_level: int | None
    features: list[str]
    tags: list[str]

    # Audit fields
    created_at: datetime
    updated_at: datetime
    created_by: str | None
    updated_by: str | None

    model_config = ConfigDict(from_attributes=True)
