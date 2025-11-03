"""Restaurant schemas.

This package contains schemas for restaurant operations.
"""

from app.domains.restaurants.schemas.restaurant.create import (
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
)
from app.domains.restaurants.schemas.restaurant.delete import (
    DeleteRestaurantSchemaRequest,
)
from app.domains.restaurants.schemas.restaurant.get import GetRestaurantSchemaResponse
from app.domains.restaurants.schemas.restaurant.list import (
    ListRestaurantsSchemaItem,
    ListRestaurantsSchemaResponse,
)
from app.domains.restaurants.schemas.restaurant.ownership import (
    AssignOwnerSchemaRequest,
    ListMyRestaurantsSchemaItem,
    ListMyRestaurantsSchemaResponse,
    ListOwnershipsSchemaResponse,
    OwnershipSchemaResponse,
    UpdateOwnerRoleSchemaRequest,
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
