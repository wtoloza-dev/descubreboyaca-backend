"""Restaurant schemas.

This package contains schemas for restaurant operations.
"""

from app.domains.restaurants.schemas.restaurant.admin.assign_owner import (
    AssignOwnerSchemaRequest,
)
from app.domains.restaurants.schemas.restaurant.admin.create import (
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
)
from app.domains.restaurants.schemas.restaurant.admin.delete import (
    DeleteRestaurantSchemaRequest,
)
from app.domains.restaurants.schemas.restaurant.admin.list_owners import (
    ListOwnershipsSchemaResponse,
)
from app.domains.restaurants.schemas.restaurant.admin.update_owner_role import (
    UpdateOwnerRoleSchemaRequest,
)
from app.domains.restaurants.schemas.restaurant.common.ownership import (
    OwnershipSchemaResponse,
)
from app.domains.restaurants.schemas.restaurant.owner.list_my_restaurants import (
    ListMyRestaurantsSchemaItem,
    ListMyRestaurantsSchemaResponse,
)
from app.domains.restaurants.schemas.restaurant.public.find_all import (
    ListRestaurantsSchemaItem,
    ListRestaurantsSchemaResponse,
)
from app.domains.restaurants.schemas.restaurant.public.get import (
    GetRestaurantSchemaResponse,
)


__all__ = [
    # Create
    "CreateRestaurantSchemaRequest",
    "CreateRestaurantSchemaResponse",
    # Delete
    "DeleteRestaurantSchemaRequest",
    # Get
    "GetRestaurantSchemaResponse",
    # List
    "ListRestaurantsSchemaItem",
    "ListRestaurantsSchemaResponse",
    # Ownership
    "AssignOwnerSchemaRequest",
    "ListMyRestaurantsSchemaItem",
    "ListMyRestaurantsSchemaResponse",
    "ListOwnershipsSchemaResponse",
    "OwnershipSchemaResponse",
    "UpdateOwnerRoleSchemaRequest",
]
