"""Restaurants domain.

This package contains all components related to the restaurants business domain,
following Domain-Driven Design principles with entities, repositories, services,
and interfaces.
"""

from app.domains.restaurants.domain import (
    CuisineType,
    PriceLevel,
    Restaurant,
    RestaurantData,
    RestaurantFeature,
)
from app.domains.restaurants.models.restaurant import RestaurantModel
from app.domains.restaurants.repositories import (
    PostgreSQLRestaurantRepository,
    SQLiteRestaurantRepository,
)
from app.domains.restaurants.routes import router
from app.domains.restaurants.schemas.restaurant.admin.create import (
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
)
from app.domains.restaurants.services import RestaurantService


__all__ = [
    # Entities
    "Restaurant",
    "RestaurantData",
    # Models
    "RestaurantModel",
    # Enums
    "CuisineType",
    "PriceLevel",
    "RestaurantFeature",
    # Repositories
    "SQLiteRestaurantRepository",
    "PostgreSQLRestaurantRepository",
    # Services
    "RestaurantService",
    # Schemas
    "CreateRestaurantSchemaRequest",
    "CreateRestaurantSchemaResponse",
    # Routes
    "router",
]
