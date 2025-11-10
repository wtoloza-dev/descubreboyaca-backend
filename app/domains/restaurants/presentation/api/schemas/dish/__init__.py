"""Dish schemas.

This package contains schemas for dish operations.
"""

from app.domains.restaurants.presentation.api.schemas.dish.admin.create import (
    CreateDishSchemaRequest,
    CreateDishSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.dish.admin.update import (
    UpdateDishSchemaRequest,
)
from app.domains.restaurants.presentation.api.schemas.dish.public.find_all import (
    FindDishesSchemaItem,
    FindDishesSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.dish.public.find_by_id import (
    FindDishSchemaResponse,
)


__all__ = [
    # Create
    "CreateDishSchemaRequest",
    "CreateDishSchemaResponse",
    # Update
    "UpdateDishSchemaRequest",
    # Find
    "FindDishSchemaResponse",
    "FindDishesSchemaItem",
    "FindDishesSchemaResponse",
]
