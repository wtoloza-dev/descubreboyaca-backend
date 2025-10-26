"""Restaurant API schemas (DTOs).

This package contains Data Transfer Objects for restaurant API endpoints.
"""

from app.domains.restaurants.schemas.create import (
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
)
from app.domains.restaurants.schemas.delete import DeleteRestaurantSchemaRequest
from app.domains.restaurants.schemas.get import GetRestaurantSchemaResponse
from app.domains.restaurants.schemas.list import (
    ListRestaurantsSchemaResponse,
    RestaurantSchemaListItem,
)
from app.domains.restaurants.schemas.ownership import (
    AssignOwnerSchemaRequest,
    MyRestaurantSchemaItem,
    MyRestaurantsSchemaResponse,
    OwnershipListSchemaResponse,
    OwnershipSchemaResponse,
    UpdateOwnerRoleSchemaRequest,
)


__all__ = [
    "AssignOwnerSchemaRequest",
    "CreateRestaurantSchemaRequest",
    "CreateRestaurantSchemaResponse",
    "DeleteRestaurantSchemaRequest",
    "GetRestaurantSchemaResponse",
    "ListRestaurantsSchemaResponse",
    "MyRestaurantSchemaItem",
    "MyRestaurantsSchemaResponse",
    "OwnershipListSchemaResponse",
    "OwnershipSchemaResponse",
    "RestaurantSchemaListItem",
    "UpdateOwnerRoleSchemaRequest",
]
