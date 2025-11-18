"""Restaurant subdomain dependencies.

This module exports all dependency injection factories for the restaurant subdomain,
including repositories and use cases.
"""

from app.domains.restaurants.infrastructure.dependencies.restaurant.repository import (
    get_restaurant_repository_dependency,
)
from app.domains.restaurants.infrastructure.dependencies.restaurant.use_cases import (
    get_count_restaurants_use_case_dependency,
    get_create_restaurant_use_case_dependency,
    get_delete_restaurant_use_case_dependency,
    get_find_restaurant_by_id_use_case_dependency,
    get_find_restaurants_use_case_dependency,
    get_list_restaurants_by_city_use_case_dependency,
    get_list_user_favorite_restaurants_use_case_dependency,
    get_update_restaurant_use_case_dependency,
)


__all__ = [
    # Repository
    "get_restaurant_repository_dependency",
    # Use Cases
    "get_count_restaurants_use_case_dependency",
    "get_create_restaurant_use_case_dependency",
    "get_delete_restaurant_use_case_dependency",
    "get_find_restaurant_by_id_use_case_dependency",
    "get_find_restaurants_use_case_dependency",
    "get_list_restaurants_by_city_use_case_dependency",
    "get_list_user_favorite_restaurants_use_case_dependency",
    "get_update_restaurant_use_case_dependency",
]
