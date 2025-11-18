"""Restaurant owner subdomain dependencies.

This module exports all dependency injection factories for the restaurant owner subdomain,
including repositories and use cases.
"""

from app.domains.restaurants.infrastructure.dependencies.restaurant_owner.repository import (
    get_restaurant_owner_repository_dependency,
)
from app.domains.restaurants.infrastructure.dependencies.restaurant_owner.use_cases import (
    get_assign_owner_use_case_dependency,
    get_check_is_owner_use_case_dependency,
    get_get_owners_by_restaurant_use_case_dependency,
    get_get_primary_owner_use_case_dependency,
    get_get_restaurants_by_owner_use_case_dependency,
    get_list_restaurant_owners_use_case_dependency,
    get_list_user_restaurants_use_case_dependency,
    get_remove_owner_use_case_dependency,
    get_require_ownership_use_case_dependency,
    get_transfer_primary_ownership_use_case_dependency,
    get_update_owner_role_use_case_dependency,
    get_verify_ownership_use_case_dependency,
)


__all__ = [
    # Repository
    "get_restaurant_owner_repository_dependency",
    # Use Cases
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
