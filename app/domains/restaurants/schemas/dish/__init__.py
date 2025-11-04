"""Dish schemas.

This package contains schemas for dish operations.
"""

from app.domains.restaurants.schemas.dish.admin.create import (
    CreateDishSchemaRequest,
    CreateDishSchemaResponse,
)
from app.domains.restaurants.schemas.dish.admin.update import UpdateDishSchemaRequest
from app.domains.restaurants.schemas.dish.public.find_all import (
    ListDishesSchemaItem,
    ListDishesSchemaResponse,
)
from app.domains.restaurants.schemas.dish.public.get import GetDishSchemaResponse


__all__ = [
    # Create
    "CreateDishSchemaRequest",
    "CreateDishSchemaResponse",
    # Update
    "UpdateDishSchemaRequest",
    # Get
    "GetDishSchemaResponse",
    # List
    "ListDishesSchemaItem",
    "ListDishesSchemaResponse",
]
