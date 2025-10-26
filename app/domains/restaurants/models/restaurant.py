"""Restaurant database model.

This module defines the Restaurant ORM model for database operations.
"""

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from app.shared.models import AuditMixin


class RestaurantModel(AuditMixin, SQLModel, table=True):
    """Restaurant database model.

    Represents a restaurant entity in the database with full audit trail.
    Inherits ULID-based id, timestamp and user tracking fields from AuditMixin.

    Note: Following DDD principles, the ID and timestamps must be provided
    by the Restaurant domain entity. This model only persists the data.

    When a restaurant is deleted, it's archived in the 'archive' table
    and removed from this table.

    Attributes:
        id: ULID primary key (inherited from AuditMixin, must be provided)
        name: Restaurant name
        description: Optional description
        address: Full street address
        city: City or municipality
        state: Department (defaults to Boyacá)
        postal_code: Optional postal/zip code
        country: Country (defaults to Colombia)
        phone: Contact phone number (required)
        email: Contact email
        website: Restaurant website URL
        location: JSON object with geographic coordinates (latitude/longitude)
        social_media: JSON object with social media links
        establishment_types: JSON array with establishment types
        cuisine_types: JSON array with cuisine types
        price_level: Price range (1-4, optional)
        features: JSON array with features/amenities
        tags: JSON array with additional tags
        created_at: Timestamp when created (inherited from AuditMixin)
        updated_at: Timestamp when updated (inherited from AuditMixin)
        created_by: ULID of creator (inherited from AuditMixin)
        updated_by: ULID of last updater (inherited from AuditMixin)
    """

    __tablename__ = "restaurants"

    # Basic information
    name: str = Field(max_length=255, nullable=False, index=True)
    description: str | None = Field(default=None, max_length=1000)

    # Address components
    address: str = Field(max_length=500, nullable=False)
    city: str = Field(max_length=100, nullable=False, index=True)
    state: str = Field(default="Boyacá", max_length=100, nullable=False)
    postal_code: str | None = Field(default=None, max_length=20)
    country: str = Field(default="Colombia", max_length=100, nullable=False)

    # Contact information
    phone: str = Field(max_length=20, nullable=False)
    email: str | None = Field(default=None, max_length=255)
    website: str | None = Field(default=None, max_length=500)

    # Geolocation (stored as JSON)
    location: dict[str, float] | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Geographic coordinates as JSON object with latitude/longitude",
    )

    # Social media (stored as JSON)
    social_media: dict[str, str] | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Social media profile URLs as JSON object",
    )

    # Business classification and categorization (stored as JSON)
    establishment_types: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, server_default="[]"),
        description="Array of establishment types (restaurant, cafe, bakery, bar, food_truck)",
    )
    cuisine_types: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, server_default="[]"),
        description="Array of cuisine types offered",
    )
    price_level: int | None = Field(
        default=None,
        ge=1,
        le=4,
        description="Price range: 1=budget, 2=moderate, 3=expensive, 4=luxury",
    )
    features: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, server_default="[]"),
        description="Array of features/amenities",
    )
    tags: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, server_default="[]"),
        description="Array of additional tags for flexible categorization",
    )
