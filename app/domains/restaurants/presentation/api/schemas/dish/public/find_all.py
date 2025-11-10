"""Dish schemas for find all endpoint.

This module defines schemas for finding all dishes with pagination.
Corresponds to: routes/dish/public/find_all.py
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.shared.schemas import PaginationSchemaData, PaginationSchemaResponse


class FindDishesSchemaItem(BaseModel):
    """Dish item in find dishes response.

    Returns essential information for finding dishes.

    Attributes:
        id: Unique dish identifier (ULID)
        restaurant_id: ID of the restaurant
        name: Dish name
        description: Short description
        category: Category
        price: Current price in COP
        original_price: Original price if discounted
        is_available: Whether dish is available
        image_url: URL to dish image
        dietary_restrictions: Dietary tags
        flavor_profile: Flavor characteristics
        is_featured: Whether dish is featured
        display_order: Display order
    """

    model_config = ConfigDict(from_attributes=True)

    # System fields
    id: str = Field(description="Unique dish identifier (ULID)")
    restaurant_id: str = Field(description="ID of the restaurant")

    # Essential fields
    name: str = Field(description="Dish name")
    description: str | None = Field(None, description="Short description")
    category: str = Field(description="Category")
    price: Decimal = Field(description="Current price in COP")
    original_price: Decimal | None = Field(
        None, description="Original price if discounted"
    )
    is_available: bool = Field(description="Whether dish is available")
    image_url: HttpUrl | None = Field(None, description="URL to dish image")
    dietary_restrictions: list[str] = Field(
        default_factory=list, description="Dietary tags"
    )
    flavor_profile: dict[str, str] = Field(
        default_factory=dict, description="Flavor characteristics"
    )
    is_featured: bool = Field(description="Whether dish is featured")
    display_order: int = Field(description="Display order")


class FindDishesSchemaResponse(PaginationSchemaResponse[FindDishesSchemaItem]):
    """Paginated response for find dishes endpoint.

    Attributes:
        data: List of dishes
        pagination: Pagination metadata

    Example:
        {
            "data": [
                {
                    "id": "01HQZX123456789ABCDEFGHIJK",
                    "name": "Ajiaco Santafereño",
                    "category": "main_course",
                    "price": 28000,
                    ...
                }
            ],
            "pagination": {
                "page": 1,
                "page_size": 20,
                "total": 42
            }
        }
    """

    data: list[FindDishesSchemaItem] = Field(description="List of dishes")
    pagination: PaginationSchemaData = Field(description="Pagination metadata")
