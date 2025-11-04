"""Find my restaurants schemas.

This module contains schemas for finding restaurants owned by the current user.
Corresponds to: routes/restaurant/owner/find_my_restaurants.py
"""

from pydantic import BaseModel, Field


class FindMyRestaurantsSchemaItem(BaseModel):
    """Restaurant item in owner's restaurant find response.

    Attributes:
        restaurant_id: Restaurant ULID
        restaurant_name: Restaurant name
        role: Owner's role in restaurant
        is_primary: Whether primary owner
        city: City or municipality
        state: State or department

    Example:
        {
            "restaurant_id": "01HKJZW8X...",
            "restaurant_name": "Mi Restaurante",
            "role": "owner",
            "is_primary": true,
            "city": "Tunja",
            "state": "Boyacá"
        }
    """

    restaurant_id: str = Field(description="Restaurant ULID")
    restaurant_name: str = Field(description="Restaurant name")
    role: str = Field(description="Owner's role in restaurant")
    is_primary: bool = Field(description="Whether primary owner")
    city: str = Field(description="City or municipality")
    state: str = Field(description="State or department")


class FindMyRestaurantsSchemaResponse(BaseModel):
    """Response schema for owner's restaurant find.

    Attributes:
        items: List of restaurants owned by user
        total: Total number of restaurants

    Example:
        {
            "items": [
                {
                    "restaurant_id": "01HKJZW8X...",
                    "restaurant_name": "Mi Restaurante",
                    ...
                }
            ],
            "total": 5
        }
    """

    items: list[FindMyRestaurantsSchemaItem] = Field(description="List of restaurants")
    total: int = Field(description="Total number of restaurants")


__all__ = ["FindMyRestaurantsSchemaItem", "FindMyRestaurantsSchemaResponse"]
