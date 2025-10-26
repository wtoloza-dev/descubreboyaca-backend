"""Dish schemas for get endpoint.

This module defines schemas for retrieving a single dish.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.shared.schemas import AuditSchema


class GetDishSchemaResponse(AuditSchema, BaseModel):
    """Response schema for get dish endpoint.

    Returns complete dish information with audit fields inherited from AuditSchema.
    """

    model_config = ConfigDict(from_attributes=True)

    # System fields (id, created_at, updated_at, etc. inherited from AuditSchema)
    restaurant_id: str = Field(
        ..., description="ID of the restaurant this dish belongs to"
    )

    # Business fields
    name: str = Field(..., description="Dish name")
    description: str | None = Field(None, description="Detailed description")
    category: str = Field(..., description="Category")
    price: Decimal = Field(..., description="Current price in COP")
    original_price: Decimal | None = Field(
        None, description="Original price before discount"
    )
    is_available: bool = Field(..., description="Whether dish is available")
    preparation_time_minutes: int | None = Field(
        None, description="Preparation time in minutes"
    )
    serves: int | None = Field(None, description="Number of people served")
    calories: int | None = Field(None, description="Estimated calories")
    image_url: HttpUrl | None = Field(None, description="URL to dish image")
    dietary_restrictions: list[str] = Field(
        default_factory=list, description="Dietary tags"
    )
    ingredients: list[str] = Field(default_factory=list, description="Main ingredients")
    allergens: list[str] = Field(default_factory=list, description="Allergens")
    flavor_profile: dict[str, str] = Field(
        default_factory=dict, description="Flavor characteristics"
    )
    is_featured: bool = Field(..., description="Whether dish is featured")
    display_order: int = Field(..., description="Display order in menu")
