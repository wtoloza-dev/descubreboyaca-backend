"""Common base schemas for dish operations.

These schemas are shared across admin and owner dish operations.
"""

from decimal import Decimal

from pydantic import BaseModel, Field, HttpUrl


class CreateDishSchemaRequest(BaseModel):
    """Request schema for creating a new dish.

    This schema is shared between admin and owner create operations.
    The restaurant_id comes from the URL path parameter.

    Example:
        {
            "name": "Ajiaco Santafereño",
            "description": "Traditional Colombian chicken soup with three types of potatoes",
            "category": "main_course",
            "price": 28000,
            "ingredients": ["chicken", "potatoes", "corn", "guascas"],
            "allergens": [],
            "flavor_profile": {"savory": "high", "hearty": "high", "creamy": "medium"},
            "is_available": true
        }
    """

    # Essential fields
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Dish name",
        examples=["Ajiaco Santafereño"],
    )

    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Category (appetizer, main_course, dessert, beverage, etc.)",
        examples=["main_course"],
    )

    price: Decimal = Field(
        ...,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Current price in local currency (COP)",
        examples=[28000],
    )

    # Optional fields
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Detailed description of the dish",
        examples=["Traditional Colombian chicken soup with three types of potatoes"],
    )

    original_price: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
        description="Original price before discount",
        examples=[35000],
    )

    is_available: bool = Field(
        default=True,
        description="Whether the dish is currently available for ordering",
    )

    preparation_time_minutes: int | None = Field(
        default=None,
        ge=0,
        le=600,
        description="Estimated preparation time in minutes",
        examples=[30],
    )

    serves: int | None = Field(
        default=None,
        ge=1,
        le=50,
        description="Number of people this dish serves",
        examples=[2],
    )

    calories: int | None = Field(
        default=None,
        ge=0,
        le=10000,
        description="Estimated calories",
        examples=[450],
    )

    image_url: HttpUrl | None = Field(
        default=None,
        description="URL to dish image",
        examples=["https://example.com/images/ajiaco.jpg"],
    )

    dietary_restrictions: list[str] = Field(
        default_factory=list,
        description="Dietary tags (vegetarian, vegan, gluten_free, lactose_free, etc.)",
        examples=[["gluten_free", "dairy_free"]],
    )

    ingredients: list[str] = Field(
        default_factory=list,
        description="List of main ingredients",
        examples=[["chicken", "potatoes", "corn", "guascas"]],
    )

    allergens: list[str] = Field(
        default_factory=list,
        description="List of allergens (nuts, dairy, shellfish, gluten, etc.)",
        examples=[[]],
    )

    flavor_profile: dict[str, str] = Field(
        default_factory=dict,
        description="Flavor characteristics with intensity levels",
        examples=[{"savory": "high", "hearty": "high", "creamy": "medium"}],
    )

    is_featured: bool = Field(
        default=False,
        description="Whether this dish should be featured/highlighted",
    )

    display_order: int = Field(
        default=0,
        ge=0,
        description="Order for displaying in menus (lower numbers appear first)",
        examples=[0],
    )


class UpdateDishSchemaRequest(BaseModel):
    """Request schema for updating an existing dish.

    This schema is shared between admin and owner update operations.
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
