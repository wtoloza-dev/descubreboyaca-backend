"""Dish schemas.

This package contains schemas for dish operations.
"""

from app.domains.restaurants.schemas.dish.create import (
    CreateDishSchemaRequest,
    CreateDishSchemaResponse,
)
from app.domains.restaurants.schemas.dish.get import GetDishSchemaResponse
from app.domains.restaurants.schemas.dish.list import (
    DishSchemaListItem,
    ListDishesSchemaResponse,
)
from app.domains.restaurants.schemas.dish.update import UpdateDishSchemaRequest


__all__ = [
    # Create
    "CreateDishSchemaRequest",
    "CreateDishSchemaResponse",
    # Update
    "UpdateDishSchemaRequest",
    # Get
    "GetDishSchemaResponse",
    # List
    "DishSchemaListItem",
    "ListDishesSchemaResponse",
]
