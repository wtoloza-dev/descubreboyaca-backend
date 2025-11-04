"""Find my restaurant schemas.

This module contains schemas for finding a restaurant owned by the current user.
Corresponds to: routes/restaurant/owner/find_my_restaurant.py
"""

from pydantic import BaseModel, ConfigDict

from app.shared.domain import GeoLocation, SocialMedia
from app.shared.schemas import AuditSchema


class FindMyRestaurantSchemaResponse(AuditSchema, BaseModel):
    """Response schema for finding my restaurant details (owner).

    Returns complete restaurant information including audit fields.
    Audit fields inherited from AuditSchema.
    """

    model_config = ConfigDict(from_attributes=True)

    # Basic information
    name: str
    description: str | None

    # Location
    address: str
    city: str
    state: str
    country: str
    postal_code: str | None
    location: GeoLocation | None

    # Contact
    phone: str
    email: str | None
    website: str | None
    social_media: SocialMedia | None

    # Classification
    establishment_types: list[str]
    cuisine_types: list[str]
    price_level: int | None

    # Features
    features: list[str]
    tags: list[str]


__all__ = ["FindMyRestaurantSchemaResponse"]
