"""Dish domain entities following DDD principles.

This module defines the Dish domain entities following DDD principles.
Dishes represent individual menu items that belong to restaurants.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.shared.domain.entities import Audit


class DishData(BaseModel):
    """Dish data fields without system metadata.

    Contains only the core business data needed to create or update a dish,
    without system-generated metadata like ID or timestamps.

    Attributes:
        restaurant_id: ID of the restaurant this dish belongs to
        name: Dish name
        description: Detailed description of the dish
        category: Primary category (appetizer, main_course, dessert, etc.)
        price: Price in local currency (COP)
        original_price: Original price before discount (for promotional pricing)
        is_available: Whether the dish is currently available for ordering
        preparation_time_minutes: Estimated preparation time in minutes
        serves: Number of people this dish serves
        calories: Estimated calories (optional)
        image_url: URL to dish image
        dietary_restrictions: List of dietary tags (vegetarian, vegan, gluten_free, etc.)
        ingredients: List of main ingredients
        allergens: List of allergens present (nuts, dairy, shellfish, etc.)
        flavor_profile: Flavor characteristics with intensity levels (e.g., {"spicy": "hot", "savory": "high"})
        is_featured: Whether this dish should be featured/highlighted
        display_order: Order for displaying in menus (lower numbers first)
    """

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    # Restaurant relationship
    restaurant_id: str = Field(
        ..., description="ID of the restaurant this dish belongs to"
    )

    # Basic information
    name: str = Field(..., min_length=1, max_length=255, description="Dish name")
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Detailed description of the dish, ingredients, and preparation",
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Primary category (appetizer, main_course, dessert, beverage, etc.)",
    )

    # Pricing
    price: Decimal = Field(
        ...,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Current price in local currency (COP)",
    )
    original_price: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Original price before discount (if on sale)",
    )

    # Availability
    is_available: bool = Field(
        default=True, description="Whether the dish is currently available for ordering"
    )

    # Additional details
    preparation_time_minutes: int | None = Field(
        default=None,
        ge=0,
        le=600,  # Max 10 hours
        description="Estimated preparation time in minutes",
    )
    serves: int | None = Field(
        default=None,
        ge=1,
        le=50,
        description="Number of people this dish serves",
    )
    calories: int | None = Field(
        default=None, ge=0, le=10000, description="Estimated calories"
    )

    # Media
    image_url: HttpUrl | None = Field(default=None, description="URL to dish image")

    # Dietary information (stored as JSON arrays)
    dietary_restrictions: list[str] = Field(
        default_factory=list,
        description="Dietary tags (vegetarian, vegan, gluten_free, lactose_free, etc.)",
    )
    ingredients: list[str] = Field(
        default_factory=list, description="List of main ingredients"
    )
    allergens: list[str] = Field(
        default_factory=list,
        description="List of allergens (nuts, dairy, shellfish, gluten, etc.)",
    )

    # Flavor profile (stored as JSON object)
    flavor_profile: dict[str, str] = Field(
        default_factory=dict,
        description="Flavor characteristics with intensity levels. Keys: flavor (spicy, sweet, salty, savory, crispy, creamy, tangy, rich, hearty, etc.). Values: intensity (none, low, medium, high, extreme) or boolean (yes)",
    )

    # Display options
    is_featured: bool = Field(
        default=False, description="Whether this dish should be featured/highlighted"
    )
    display_order: int = Field(
        default=0,
        ge=0,
        description="Order for displaying in menus (lower numbers appear first)",
    )


class Dish(DishData, Audit):
    """Complete Dish entity with system metadata.

    Extends DishData with database primary key and audit fields.
    The entity generates its own identity (ULID) and timestamps following DDD principles.

    This is the complete domain entity that includes both business data and system metadata.
    Use this when working with persisted dishes that already have an ID.

    Attributes:
        id: ULID primary key (auto-generated, inherited from Audit)
        created_at: Timestamp when created (auto-generated, inherited from Audit)
        updated_at: Timestamp when updated (auto-generated, inherited from Audit)
        created_by: ULID of creator (inherited from Audit)
        updated_by: ULID of last updater (inherited from Audit)
    """
