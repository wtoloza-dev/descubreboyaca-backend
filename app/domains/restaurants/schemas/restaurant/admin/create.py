"""Restaurant schemas for create endpoint.

This module defines schemas for creating restaurants and their responses.
Corresponds to: routes/restaurant/admin/create.py
"""

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain import GeoLocation, SocialMedia
from app.shared.schemas import AuditSchema


class CreateRestaurantSchemaRequest(BaseModel):
    """Simplified request schema for creating a new restaurant.

    This schema includes only the essential fields needed to create a restaurant.
    Additional details can be added later through update operations.

    Example:
        {
            "name": "La Casona Boyacense",
            "address": "Calle 20 #10-52",
            "city": "Tunja",
            "phone": "+573001234567",
            "description": "Restaurante típico de comida boyacense"
        }

        Or with location:
        {
            "name": "La Casona Boyacense",
            "address": "Calle 20 #10-52",
            "city": "Tunja",
            "phone": "+573001234567",
            "location": {
                "latitude": 5.5353,
                "longitude": -73.3678
            }
        }
    """

    # Essential fields
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Restaurant name",
        examples=["La Casona Boyacense"],
    )

    address: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Full street address",
        examples=["Calle 20 #10-52"],
    )

    city: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="City or municipality",
        examples=["Tunja", "Duitama", "Sogamoso", "Paipa"],
    )

    phone: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Contact phone number (required)",
        examples=["+573001234567", "3001234567"],
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Brief description of the restaurant",
        examples=["Restaurante típico de comida boyacense"],
    )

    location: GeoLocation | None = Field(
        default=None,
        description="GPS coordinates of the restaurant",
    )


class CreateRestaurantSchemaResponse(AuditSchema, BaseModel):
    """Response schema for create restaurant endpoint.

    Audit fields (id, created_at, updated_at, created_by, updated_by) are inherited from AuditSchema.
    """

    # System fields (id, created_at, updated_at, etc. inherited from AuditSchema)

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

    model_config = ConfigDict(from_attributes=True)
