"""Restaurant API schemas (DTOs).

This package contains Data Transfer Objects for restaurant API endpoints.
"""

from app.domains.restaurants.schemas.restaurant import (
    AssignOwnerSchemaRequest,
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
    DeleteRestaurantSchemaRequest,
    GetRestaurantSchemaResponse,
    ListRestaurantsSchemaResponse,
    MyRestaurantSchemaItem,
    MyRestaurantsSchemaResponse,
    OwnershipListSchemaResponse,
    OwnershipSchemaResponse,
    RestaurantSchemaListItem,
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
