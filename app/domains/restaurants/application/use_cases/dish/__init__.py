"""Dish use cases.

This package contains all use cases related to dish operations.
Each use case represents a single business operation.
"""

from .create_dish import (
    CreateDishUseCase,
)
from .delete_dish import (
    DeleteDishUseCase,
)
from .find_dish_by_id import (
    FindDishByIdUseCase,
)
from .list_dishes import (
    ListDishesUseCase,
)
from .list_restaurant_dishes import (
    ListRestaurantDishesUseCase,
)
from .toggle_dish_availability import (
    ToggleDishAvailabilityUseCase,
)
from .update_dish import (
    UpdateDishUseCase,
)


__all__ = [
    "CreateDishUseCase",
    "DeleteDishUseCase",
    "FindDishByIdUseCase",
    "ListDishesUseCase",
    "ListRestaurantDishesUseCase",
    "ToggleDishAvailabilityUseCase",
    "UpdateDishUseCase",
]
