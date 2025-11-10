"""Update my restaurant schemas.

This module contains request and response schemas for updating restaurant details.
Corresponds to: routes/restaurant/owner/update_my_restaurant.py
"""

from pydantic import BaseModel, ConfigDict, Field

from app.shared.domain import GeoLocation, SocialMedia
from app.shared.schemas import AuditSchema


class UpdateMyRestaurantSchemaRequest(BaseModel):
    """Request schema for updating restaurant (owner).

    All fields are optional - only provided fields will be updated.
    """

    name: str | None = Field(default=None, description="Restaurant name")
    description: str | None = Field(default=None, description="Restaurant description")
    address: str | None = Field(default=None, description="Physical address")
    city: str | None = Field(default=None, description="City")
    state: str | None = Field(default=None, description="State/department")
    country: str | None = Field(default=None, description="Country")
    postal_code: str | None = Field(default=None, description="Postal code")
    location: GeoLocation | None = Field(default=None, description="GPS coordinates")
    phone: str | None = Field(default=None, description="Contact phone")
    email: str | None = Field(default=None, description="Contact email")
    website: str | None = Field(default=None, description="Website URL")
    social_media: SocialMedia | None = Field(
        default=None, description="Social media links"
    )
    establishment_types: list[str] | None = Field(
        default=None, description="Establishment types"
    )
    cuisine_types: list[str] | None = Field(default=None, description="Cuisine types")
    price_level: int | None = Field(
        default=None, ge=1, le=4, description="Price level (1-4)"
    )
    features: list[str] | None = Field(default=None, description="Features/amenities")
    tags: list[str] | None = Field(default=None, description="Tags")


class UpdateMyRestaurantSchemaResponse(AuditSchema, BaseModel):
    """Response schema for updated restaurant (owner).

    Returns complete restaurant information including audit fields.
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


__all__ = ["UpdateMyRestaurantSchemaRequest", "UpdateMyRestaurantSchemaResponse"]
