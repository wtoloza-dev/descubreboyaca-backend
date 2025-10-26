"""Restaurant domain entities.

This module defines the Restaurant domain entities following DDD principles.
"""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.shared.domain import Audit, GeoLocation, SocialMedia


class RestaurantData(BaseModel):
    """Restaurant data fields without system metadata.

    Contains only the core business data needed to create or update a restaurant,
    without system-generated metadata like ID or timestamps.

    Attributes:
        name: Restaurant name
        description: Optional detailed description
        address: Full street address
        city: City or municipality
        state: Department (e.g., Boyacá)
        postal_code: Optional postal/zip code
        country: Country (defaults to Colombia)
        phone: Contact phone number (optional, but recommended)
        email: Contact email address
        website: Restaurant website URL
        location: Geographic coordinates for maps (optional, can be geocoded from address)
        social_media: Social media profile links
        establishment_types: List of establishment types (restaurant, cafe, bakery, bar, etc.)
        cuisine_types: List of cuisine types offered
        price_level: Price range indicator (1=budget, 2=moderate, 3=expensive, 4=luxury)
        features: List of features/amenities
        tags: Additional tags for flexible categorization (romantic, family_friendly, etc.)
    """

    model_config = ConfigDict(from_attributes=True)

    # Basic information
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)

    # Address components
    address: str = Field(..., min_length=1, max_length=500)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(default="Boyacá", max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    country: str = Field(default="Colombia", max_length=100)

    # Contact information
    phone: str = Field(..., max_length=20)
    email: str | None = Field(default=None, max_length=255)
    website: HttpUrl | None = None

    # Geolocation (optional, can be added later via geocoding)
    location: GeoLocation | None = None

    # Social media
    social_media: SocialMedia | None = None

    # Business classification and categorization
    establishment_types: list[str] = Field(
        default_factory=list,
        description="Type of establishment (e.g., 'restaurant', 'cafe', 'bakery', 'bar', 'food_truck')",
    )
    cuisine_types: list[str] = Field(
        default_factory=list,
        description="Types of cuisine offered (e.g., 'colombiana', 'boyacense', 'internacional')",
    )
    price_level: int | None = Field(
        default=None,
        ge=1,
        le=4,
        description="Price range: 1=budget, 2=moderate, 3=expensive, 4=luxury",
    )
    features: list[str] = Field(
        default_factory=list,
        description="Features/amenities (e.g., 'wifi', 'parking', 'pet_friendly', 'outdoor_seating')",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Additional tags for flexible categorization (e.g., 'romantic', 'family_friendly', 'instagram_worthy', 'mountain_view')",
    )


class Restaurant(Audit, RestaurantData):
    """Restaurant entity with database identity and audit trail.

    Extends RestaurantData with database primary key and audit fields.
    The entity generates its own identity (ULID) and timestamps following DDD principles.

    This is the complete domain entity that includes both business data and system metadata.
    Use this when working with persisted restaurants that already have an ID.

    Attributes:
        id: ULID primary key (auto-generated, inherited from Audit)
        created_at: Timestamp when created (auto-generated, inherited from Audit)
        updated_at: Timestamp when updated (auto-generated, inherited from Audit)
        created_by: ULID of creator (inherited from Audit)
        updated_by: ULID of last updater (inherited from Audit)
        [All RestaurantData fields inherited]

    Note:
        No custom serialization needed! Pydantic automatically converts:
        - GeoLocation (Decimal) → dict[str, float]
        - SocialMedia → dict[str, str]
        - HttpUrl → str
    """
