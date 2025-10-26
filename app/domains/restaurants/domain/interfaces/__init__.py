"""Restaurant repository interfaces (Protocols).

This package contains protocol interfaces for restaurant repositories.
"""

from app.domains.restaurants.domain.interfaces.dish import DishRepositoryInterface
from app.domains.restaurants.domain.interfaces.restaurant import (
    RestaurantRepositoryInterface,
)
from app.domains.restaurants.domain.interfaces.restaurant_owner import (
    RestaurantOwnerRepositoryInterface,
)


__all__ = [
    "DishRepositoryInterface",
    "RestaurantRepositoryInterface",
    "RestaurantOwnerRepositoryInterface",
]
