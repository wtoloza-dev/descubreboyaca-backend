"""Restaurant schemas.

This package contains schemas for restaurant operations.
"""

from app.domains.restaurants.presentation.api.schemas.restaurant.admin.assign_restaurant_owner_by_admin import (
    AssignRestaurantOwnerByAdminSchemaRequest,
    AssignRestaurantOwnerByAdminSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.create_restaurant_by_admin import (
    CreateRestaurantByAdminSchemaRequest,
    CreateRestaurantByAdminSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.delete_restaurant_by_admin import (
    DeleteRestaurantByAdminSchemaRequest,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.find_restaurant_owners_by_admin import (
    FindRestaurantOwnersByAdminSchemaItem,
    FindRestaurantOwnersByAdminSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.transfer_restaurant_ownership_by_admin import (
    TransferRestaurantOwnershipByAdminSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.update_restaurant_owner_role_by_admin import (
    UpdateRestaurantOwnerRoleByAdminSchemaRequest,
    UpdateRestaurantOwnerRoleByAdminSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.owner.find_my_restaurants import (
    FindMyRestaurantsSchemaItem,
    FindMyRestaurantsSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_all_restaurants import (
    FindAllRestaurantsSchemaItem,
    FindAllRestaurantsSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_restaurant_by_id import (
    FindRestaurantByIdSchemaResponse,
)


__all__ = [
    # Admin - Create
    "CreateRestaurantByAdminSchemaRequest",
    "CreateRestaurantByAdminSchemaResponse",
    # Admin - Delete
    "DeleteRestaurantByAdminSchemaRequest",
    # Admin - Ownership
    "AssignRestaurantOwnerByAdminSchemaRequest",
    "AssignRestaurantOwnerByAdminSchemaResponse",
    "FindRestaurantOwnersByAdminSchemaItem",
    "FindRestaurantOwnersByAdminSchemaResponse",
    "TransferRestaurantOwnershipByAdminSchemaResponse",
    "UpdateRestaurantOwnerRoleByAdminSchemaRequest",
    "UpdateRestaurantOwnerRoleByAdminSchemaResponse",
    # Public - Find
    "FindRestaurantByIdSchemaResponse",
    "FindAllRestaurantsSchemaItem",
    "FindAllRestaurantsSchemaResponse",
    # Owner
    "FindMyRestaurantsSchemaItem",
    "FindMyRestaurantsSchemaResponse",
]
