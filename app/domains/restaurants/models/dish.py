"""Dish database model.

This module defines the Dish ORM model for database operations.
"""

from decimal import Decimal

from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlmodel import Field, SQLModel

from app.shared.models import AuditMixin


class DishModel(AuditMixin, SQLModel, table=True):
    """Dish database model.

    Represents a dish/menu item entity in the database with full audit trail.
    Inherits ULID-based id, timestamp and user tracking fields from AuditMixin.

    Each dish belongs to exactly one restaurant (foreign key relationship).
    When a restaurant is deleted (CASCADE), all its dishes are also deleted.

    Note: Following DDD principles, the ID and timestamps must be provided
    by the Dish domain entity. This model only persists the data.

    Attributes:
        id: ULID primary key (inherited from AuditMixin, must be provided)
        restaurant_id: Foreign key to restaurants table (ULID)
        name: Dish name
        description: Optional detailed description
        category: Primary category (appetizer, main_course, dessert, etc.)
        price: Current price (Decimal for monetary precision)
        original_price: Original price before discount (optional)
        is_available: Whether dish is currently available for ordering
        preparation_time_minutes: Estimated preparation time (optional)
        serves: Number of people served (optional)
        calories: Estimated calories (optional)
        image_url: URL to dish image (optional)
        dietary_restrictions: JSON array of dietary tags (vegetarian, vegan, etc.)
        ingredients: JSON array of main ingredients
        allergens: JSON array of allergens (nuts, dairy, shellfish, etc.)
        flavor_profile: JSON object with flavor characteristics and intensity levels
        is_featured: Whether dish should be featured/highlighted
        display_order: Order for displaying in menus (lower = first)
        created_at: Timestamp when created (inherited from AuditMixin)
        updated_at: Timestamp when updated (inherited from AuditMixin)
        created_by: ULID of creator (inherited from AuditMixin)
        updated_by: ULID of last updater (inherited from AuditMixin)
    """

    __tablename__ = "dishes"

    # Foreign key to restaurant
    restaurant_id: str = Field(
        sa_column=Column(
            String(26),
            ForeignKey("restaurants.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        description="ID of the restaurant this dish belongs to",
    )

    # Basic information
    name: str = Field(max_length=255, nullable=False, index=True)
    description: str | None = Field(default=None, max_length=2000)
    category: str = Field(max_length=50, nullable=False, index=True)

    # Pricing (using Decimal for monetary precision)
    price: Decimal = Field(
        sa_column=Column(Numeric(precision=10, scale=2), nullable=False),
        description="Current price in local currency (COP)",
    )
    original_price: Decimal | None = Field(
        default=None,
        sa_column=Column(Numeric(precision=10, scale=2), nullable=True),
        description="Original price before discount",
    )

    # Availability
    is_available: bool = Field(
        sa_column=Column(Boolean, nullable=False, server_default="true", index=True),
        description="Whether the dish is currently available for ordering",
    )

    # Additional details
    preparation_time_minutes: int | None = Field(
        default=None,
        sa_column=Column(Integer, nullable=True),
        description="Estimated preparation time in minutes",
    )
    serves: int | None = Field(
        default=None,
        sa_column=Column(Integer, nullable=True),
        description="Number of people this dish serves",
    )
    calories: int | None = Field(
        default=None,
        sa_column=Column(Integer, nullable=True),
        description="Estimated calories",
    )

    # Media
    image_url: str | None = Field(default=None, max_length=500)

    # Dietary information (stored as JSON arrays)
    dietary_restrictions: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, server_default="[]"),
        description="Array of dietary tags (vegetarian, vegan, gluten_free, etc.)",
    )
    ingredients: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, server_default="[]"),
        description="Array of main ingredients",
    )
    allergens: list[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, server_default="[]"),
        description="Array of allergens (nuts, dairy, shellfish, gluten, etc.)",
    )

    # Flavor profile (stored as JSON object)
    flavor_profile: dict[str, str] = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False, server_default="{}"),
        description="Flavor characteristics with intensity levels",
    )

    # Display options
    is_featured: bool = Field(
        sa_column=Column(Boolean, nullable=False, server_default="false", index=True),
        description="Whether this dish should be featured/highlighted",
    )
    display_order: int = Field(
        default=0,
        sa_column=Column(Integer, nullable=False, server_default="0", index=True),
        description="Order for displaying in menus (lower numbers appear first)",
    )

