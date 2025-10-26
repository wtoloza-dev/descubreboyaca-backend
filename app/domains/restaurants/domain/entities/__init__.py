"""Restaurant domain entities.

This package contains the core business entities for the restaurants domain.
Entities represent objects with identity and lifecycle.
"""

from app.domains.restaurants.domain.entities.dish import Dish, DishData
from app.domains.restaurants.domain.entities.restaurant import (
    Restaurant,
    RestaurantData,
)
from app.domains.restaurants.domain.entities.restaurant_owner import (
    RestaurantOwner,
    RestaurantOwnerData,
)


__all__ = [
    "Dish",
    "DishData",
    "Restaurant",
    "RestaurantData",
    "RestaurantOwner",
    "RestaurantOwnerData",
]
