"""Restaurant domain dependencies.

This module exports all dependency injection factories for the restaurant domain,
organized by subdomain (restaurant, dish, restaurant_owner).

Each subdomain provides:
    - Repository factories
    - Use case factories

Architecture:
    Following the Use Case pattern (not Services) for clean, atomic operations.
    Each use case has its own dependency factory following the naming convention:
    get_{entity}_{action}_use_case_dependency
"""

# Dish subdomain
from app.domains.restaurants.infrastructure.dependencies.dish import (
    get_create_dish_use_case_dependency,
    get_delete_dish_use_case_dependency,
    get_dish_repository_dependency,
    get_find_dish_by_id_use_case_dependency,
    get_list_dishes_use_case_dependency,
    get_list_restaurant_dishes_use_case_dependency,
    get_toggle_dish_availability_use_case_dependency,
    get_update_dish_use_case_dependency,
)

# Filters
from app.domains.restaurants.infrastructure.dependencies.filters import (
    RestaurantFilters,
    get_restaurant_filters_dependency,
)

# Restaurant subdomain
from app.domains.restaurants.infrastructure.dependencies.restaurant import (
    get_count_restaurants_use_case_dependency,
    get_create_restaurant_use_case_dependency,
    get_delete_restaurant_use_case_dependency,
    get_find_restaurant_by_id_use_case_dependency,
    get_find_restaurants_use_case_dependency,
    get_list_restaurants_by_city_use_case_dependency,
    get_list_user_favorite_restaurants_use_case_dependency,
    get_restaurant_repository_dependency,
    get_update_restaurant_use_case_dependency,
)

# Restaurant owner subdomain
from app.domains.restaurants.infrastructure.dependencies.restaurant_owner import (
    get_assign_owner_use_case_dependency,
    get_check_is_owner_use_case_dependency,
    get_get_owners_by_restaurant_use_case_dependency,
    get_get_primary_owner_use_case_dependency,
    get_get_restaurants_by_owner_use_case_dependency,
    get_list_restaurant_owners_use_case_dependency,
    get_list_user_restaurants_use_case_dependency,
    get_remove_owner_use_case_dependency,
    get_require_ownership_use_case_dependency,
    get_restaurant_owner_repository_dependency,
    get_transfer_primary_ownership_use_case_dependency,
    get_update_owner_role_use_case_dependency,
    get_verify_ownership_use_case_dependency,
)


__all__ = [
    # ============================================================
    # Repositories
    # ============================================================
    "get_restaurant_repository_dependency",
    "get_dish_repository_dependency",
    "get_restaurant_owner_repository_dependency",
    # ============================================================
    # Filters
    # ============================================================
    "RestaurantFilters",
    "get_restaurant_filters_dependency",
    # ============================================================
    # Restaurant Use Cases
    # ============================================================
    "get_count_restaurants_use_case_dependency",
    "get_create_restaurant_use_case_dependency",
    "get_delete_restaurant_use_case_dependency",
    "get_find_restaurant_by_id_use_case_dependency",
    "get_find_restaurants_use_case_dependency",
    "get_list_restaurants_by_city_use_case_dependency",
    "get_list_user_favorite_restaurants_use_case_dependency",
    "get_update_restaurant_use_case_dependency",
    # ============================================================
    # Dish Use Cases
    # ============================================================
    "get_create_dish_use_case_dependency",
    "get_delete_dish_use_case_dependency",
    "get_find_dish_by_id_use_case_dependency",
    "get_list_dishes_use_case_dependency",
    "get_list_restaurant_dishes_use_case_dependency",
    "get_toggle_dish_availability_use_case_dependency",
    "get_update_dish_use_case_dependency",
    # ============================================================
    # Restaurant Owner Use Cases
    # ============================================================
    "get_assign_owner_use_case_dependency",
    "get_check_is_owner_use_case_dependency",
    "get_get_owners_by_restaurant_use_case_dependency",
    "get_get_primary_owner_use_case_dependency",
    "get_get_restaurants_by_owner_use_case_dependency",
    "get_list_restaurant_owners_use_case_dependency",
    "get_list_user_restaurants_use_case_dependency",
    "get_remove_owner_use_case_dependency",
    "get_require_ownership_use_case_dependency",
    "get_transfer_primary_ownership_use_case_dependency",
    "get_update_owner_role_use_case_dependency",
    "get_verify_ownership_use_case_dependency",
]
