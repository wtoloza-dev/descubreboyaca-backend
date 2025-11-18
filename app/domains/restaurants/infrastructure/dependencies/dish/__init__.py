"""Dish subdomain dependencies.

This module exports all dependency injection factories for the dish subdomain,
including repositories and use cases.
"""

from app.domains.restaurants.infrastructure.dependencies.dish.repository import (
    get_dish_repository_dependency,
)
from app.domains.restaurants.infrastructure.dependencies.dish.use_cases import (
    get_create_dish_use_case_dependency,
    get_delete_dish_use_case_dependency,
    get_find_dish_by_id_use_case_dependency,
    get_list_dishes_use_case_dependency,
    get_list_restaurant_dishes_use_case_dependency,
    get_toggle_dish_availability_use_case_dependency,
    get_update_dish_use_case_dependency,
)


__all__ = [
    # Repository
    "get_dish_repository_dependency",
    # Use Cases
    "get_create_dish_use_case_dependency",
    "get_delete_dish_use_case_dependency",
    "get_find_dish_by_id_use_case_dependency",
    "get_list_dishes_use_case_dependency",
    "get_list_restaurant_dishes_use_case_dependency",
    "get_toggle_dish_availability_use_case_dependency",
    "get_update_dish_use_case_dependency",
]
