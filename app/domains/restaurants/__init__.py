"""Restaurants domain.

This package contains all components related to the restaurants business domain,
following Domain-Driven Design principles with entities, repositories, services,
and interfaces.
"""

from app.domains.restaurants.application.services import RestaurantService
from app.domains.restaurants.domain import (
    CuisineType,
    PriceLevel,
    Restaurant,
    RestaurantData,
    RestaurantFeature,
)
from app.domains.restaurants.infrastructure.persistence.models.restaurant import (
    RestaurantModel,
)
from app.domains.restaurants.infrastructure.persistence.repositories import (
    PostgreSQLRestaurantRepository,
    SQLiteRestaurantRepository,
)
from app.domains.restaurants.presentation.api.routes import router
from app.domains.restaurants.presentation.api.schemas.restaurant.admin.create import (
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
)


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
