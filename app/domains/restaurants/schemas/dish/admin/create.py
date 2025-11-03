"""Dish creation schemas for admin.

This module contains request and response schemas for the admin create route.
Corresponds to: routes/dish/admin/create.py
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.domains.restaurants.schemas.dish.common import CreateDishSchemaRequest
from app.shared.schemas import AuditSchema


__all__ = ["CreateDishSchemaRequest", "CreateDishSchemaResponse"]


class CreateDishSchemaResponse(AuditSchema, BaseModel):
    """Response schema for created dish (admin).

    Returns the complete dish entity with system metadata.
    Audit fields (id, created_at, updated_at, created_by, updated_by) are inherited from AuditSchema.
    """

    model_config = ConfigDict(from_attributes=True)

    # System fields (id, created_at, updated_at, etc. inherited from AuditSchema)
    restaurant_id: str = Field(
        ..., description="ID of the restaurant this dish belongs to"
    )

    # Business fields
    name: str
    description: str | None
    category: str
    price: Decimal
    original_price: Decimal | None
    is_available: bool
    preparation_time_minutes: int | None
    serves: int | None
    calories: int | None
    image_url: HttpUrl | None
    dietary_restrictions: list[str]
    ingredients: list[str]
    allergens: list[str]
    flavor_profile: dict[str, str]
    is_featured: bool
    display_order: int
