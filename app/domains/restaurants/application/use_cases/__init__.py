"""Restaurant application use cases.

This package contains all use cases for the restaurant domain,
organized by entity type. Each use case represents a single business operation
following the Single Responsibility Principle.

Architecture:
    - Each use case has a single `execute()` method
    - Dependencies are injected via constructor
    - Business logic is isolated and testable
    - No framework dependencies (FastAPI, SQLAlchemy)

Subdirectories:
    - restaurant: Use cases for restaurant operations
    - dish: Use cases for dish operations
    - restaurant_owner: Use cases for ownership operations
"""

# Restaurant use cases
# Dish use cases
from app.domains.restaurants.application.use_cases.dish import (
    CreateDishUseCase,
    DeleteDishUseCase,
    FindDishByIdUseCase,
    ListDishesUseCase,
    ListRestaurantDishesUseCase,
    ToggleDishAvailabilityUseCase,
    UpdateDishUseCase,
)
from app.domains.restaurants.application.use_cases.restaurant import (
    CountRestaurantsUseCase,
    CreateRestaurantUseCase,
    DeleteRestaurantUseCase,
    FindRestaurantByIdUseCase,
    FindRestaurantsUseCase,
    ListRestaurantsByCityUseCase,
    ListUserFavoriteRestaurantsUseCase,
    UpdateRestaurantUseCase,
)

# Restaurant owner use cases
from app.domains.restaurants.application.use_cases.restaurant_owner import (
    AssignOwnerUseCase,
    CheckIsOwnerUseCase,
    GetOwnersByRestaurantUseCase,
    GetPrimaryOwnerUseCase,
    GetRestaurantsByOwnerUseCase,
    ListRestaurantOwnersUseCase,
    ListUserRestaurantsUseCase,
    RemoveOwnerUseCase,
    RequireOwnershipUseCase,
    TransferPrimaryOwnershipUseCase,
    UpdateOwnerRoleUseCase,
    VerifyOwnershipUseCase,
)


__all__ = [
    # Restaurant use cases
    "CountRestaurantsUseCase",
    "CreateRestaurantUseCase",
    "DeleteRestaurantUseCase",
    "FindRestaurantByIdUseCase",
    "FindRestaurantsUseCase",
    "ListRestaurantsByCityUseCase",
    "ListUserFavoriteRestaurantsUseCase",
    "UpdateRestaurantUseCase",
    # Dish use cases
    "CreateDishUseCase",
    "DeleteDishUseCase",
    "FindDishByIdUseCase",
    "ListDishesUseCase",
    "ListRestaurantDishesUseCase",
    "ToggleDishAvailabilityUseCase",
    "UpdateDishUseCase",
    # Restaurant owner use cases
    "AssignOwnerUseCase",
    "CheckIsOwnerUseCase",
    "GetOwnersByRestaurantUseCase",
    "GetPrimaryOwnerUseCase",
    "GetRestaurantsByOwnerUseCase",
    "ListRestaurantOwnersUseCase",
    "ListUserRestaurantsUseCase",
    "RemoveOwnerUseCase",
    "RequireOwnershipUseCase",
    "TransferPrimaryOwnershipUseCase",
    "UpdateOwnerRoleUseCase",
    "VerifyOwnershipUseCase",
]
