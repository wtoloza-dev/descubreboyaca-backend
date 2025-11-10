"""Restaurant schemas.

This package contains schemas for restaurant operations.
"""

from app.domains.restaurants.presentation.api.schemas.restaurant.admin.assign_owner import (
    AssignOwnerSchemaRequest,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.create import (
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.delete import (
    DeleteRestaurantSchemaRequest,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.find_owners import (
    FindOwnershipsSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.update_owner_role import (
    UpdateOwnerRoleSchemaRequest,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.common.ownership import (
    OwnershipSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.owner.find_my_restaurants import (
    FindMyRestaurantsSchemaItem,
    FindMyRestaurantsSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_all import (
    FindRestaurantsSchemaItem,
    FindRestaurantsSchemaResponse,
)
from app.domains.restaurants.presentation.api.schemas.restaurant.public.find_by_id import (
    FindRestaurantSchemaResponse,
)


__all__ = [
    # Create
    "CreateRestaurantSchemaRequest",
    "CreateRestaurantSchemaResponse",
    # Delete
    "DeleteRestaurantSchemaRequest",
    # Find
    "FindRestaurantSchemaResponse",
    "FindRestaurantsSchemaItem",
    "FindRestaurantsSchemaResponse",
    # Ownership
    "AssignOwnerSchemaRequest",
    "FindMyRestaurantsSchemaItem",
    "FindMyRestaurantsSchemaResponse",
    "FindOwnershipsSchemaResponse",
    "OwnershipSchemaResponse",
    "UpdateOwnerRoleSchemaRequest",
]
