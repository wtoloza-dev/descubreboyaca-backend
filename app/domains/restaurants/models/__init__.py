"""Restaurant database models.

This package contains SQLModel ORM models for the restaurants domain.
"""

from .restaurant import RestaurantModel
from .restaurant_owner import RestaurantOwnerModel


__all__ = [
    "RestaurantModel",
    "RestaurantOwnerModel",
]
