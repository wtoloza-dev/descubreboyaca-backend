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
    ListRestaurantsSchemaResponse,
    RestaurantSchemaListItem,
)
from app.domains.restaurants.schemas.restaurant.ownership import (
    AssignOwnerSchemaRequest,
    MyRestaurantSchemaItem,
    MyRestaurantsSchemaResponse,
    OwnershipListSchemaResponse,
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
    "ListRestaurantsSchemaResponse",
    "RestaurantSchemaListItem",
    # Ownership
    "AssignOwnerSchemaRequest",
    "MyRestaurantSchemaItem",
    "MyRestaurantsSchemaResponse",
    "OwnershipListSchemaResponse",
    "OwnershipSchemaResponse",
    "UpdateOwnerRoleSchemaRequest",
]
