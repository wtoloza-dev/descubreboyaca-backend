"""Dish schemas for update endpoint.

This module defines schemas for updating dishes.
"""

from decimal import Decimal

from pydantic import BaseModel, Field, HttpUrl


class UpdateDishSchemaRequest(BaseModel):
    """Request schema for updating an existing dish.

    All fields are optional - only provided fields will be updated.

    Example:
        {
            "price": 30000,
            "is_available": false
        }
    """

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Dish name",
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Detailed description of the dish",
    )

    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Category (appetizer, main_course, dessert, beverage, etc.)",
    )

    price: Decimal | None = Field(
        default=None,
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
        description="Original price before discount",
    )

    is_available: bool | None = Field(
        default=None,
        description="Whether the dish is currently available for ordering",
    )

    preparation_time_minutes: int | None = Field(
        default=None,
        ge=0,
        le=600,
        description="Estimated preparation time in minutes",
    )

    serves: int | None = Field(
        default=None,
        ge=1,
        le=50,
        description="Number of people this dish serves",
    )

    calories: int | None = Field(
        default=None,
        ge=0,
        le=10000,
        description="Estimated calories",
    )

    image_url: HttpUrl | None = Field(
        default=None,
        description="URL to dish image",
    )

    dietary_restrictions: list[str] | None = Field(
        default=None,
        description="Dietary tags (vegetarian, vegan, gluten_free, lactose_free, etc.)",
    )

    ingredients: list[str] | None = Field(
        default=None,
        description="List of main ingredients",
    )

    allergens: list[str] | None = Field(
        default=None,
        description="List of allergens (nuts, dairy, shellfish, gluten, etc.)",
    )

    flavor_profile: dict[str, str] | None = Field(
        default=None,
        description="Flavor characteristics with intensity levels",
    )

    is_featured: bool | None = Field(
        default=None,
        description="Whether this dish should be featured/highlighted",
    )

    display_order: int | None = Field(
        default=None,
        ge=0,
        description="Order for displaying in menus (lower numbers appear first)",
    )

