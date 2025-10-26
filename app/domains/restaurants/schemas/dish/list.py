"""Dish schemas for list endpoint.

This module defines schemas for listing dishes with pagination.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.shared.schemas import PaginatedResponse


class DishSchemaListItem(BaseModel):
    """Simplified dish schema for list responses.

    Returns essential information for listing dishes.
    """

    model_config = ConfigDict(from_attributes=True)

    # System fields
    id: str = Field(..., description="Unique dish identifier (ULID)")
    restaurant_id: str = Field(..., description="ID of the restaurant")

    # Essential fields
    name: str = Field(..., description="Dish name")
    description: str | None = Field(None, description="Short description")
    category: str = Field(..., description="Category")
    price: Decimal = Field(..., description="Current price in COP")
    original_price: Decimal | None = Field(None, description="Original price if discounted")
    is_available: bool = Field(..., description="Whether dish is available")
    image_url: HttpUrl | None = Field(None, description="URL to dish image")
    dietary_restrictions: list[str] = Field(default_factory=list, description="Dietary tags")
    flavor_profile: dict[str, str] = Field(default_factory=dict, description="Flavor characteristics")
    is_featured: bool = Field(..., description="Whether dish is featured")
    display_order: int = Field(..., description="Display order")


class ListDishesSchemaResponse(PaginatedResponse[DishSchemaListItem]):
    """Paginated response for list dishes endpoint.

    Example:
        {
            "items": [
                {
                    "id": "01HQZX123456789ABCDEFGHIJK",
                    "name": "Ajiaco Santafereño",
                    "category": "main_course",
                    "price": 28000,
                    ...
                }
            ],
            "page": 1,
            "page_size": 20,
            "total": 42
        }
    """

    pass

