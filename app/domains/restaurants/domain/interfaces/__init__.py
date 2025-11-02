"""Restaurant repository interfaces (Protocols).

This package contains protocol interfaces for restaurant repositories.
"""

from .dish_repository import DishRepositoryInterface
from .restaurant_owner_repository import RestaurantOwnerRepositoryInterface
from .restaurant_repository import RestaurantRepositoryInterface


__all__ = [
    "DishRepositoryInterface",
    "RestaurantOwnerRepositoryInterface",
    "RestaurantRepositoryInterface",
]
