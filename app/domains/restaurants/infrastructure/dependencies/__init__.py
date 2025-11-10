"""Restaurant dependencies.

This module provides dependency injection factories for restaurant-related
operations.

All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from app.domains.restaurants.infrastructure.dependencies.dish import (
    get_dish_repository_dependency,
    get_dish_service_dependency,
)
from app.domains.restaurants.infrastructure.dependencies.filters import (
    RestaurantFilters,
    get_restaurant_filters_dependency,
)
from app.domains.restaurants.infrastructure.dependencies.restaurant import (
    get_restaurant_owner_repository_dependency,
    get_restaurant_owner_service_dependency,
    get_restaurant_repository_dependency,
    get_restaurant_service_dependency,
)


__all__ = [
    # Filters
    "RestaurantFilters",
    "get_restaurant_filters_dependency",
    # Restaurant
    "get_restaurant_repository_dependency",
    "get_restaurant_service_dependency",
    "get_restaurant_owner_repository_dependency",
    "get_restaurant_owner_service_dependency",
    # Dish
    "get_dish_repository_dependency",
    "get_dish_service_dependency",
]
