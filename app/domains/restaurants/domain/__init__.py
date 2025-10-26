"""Restaurants domain layer.

This package contains domain primitives and building blocks for the restaurants
bounded context: entities, value objects, enums, and constants.
"""

from app.domains.restaurants.domain.entities import (
    Dish,
    DishData,
    Restaurant,
    RestaurantData,
)
from app.domains.restaurants.domain.enums import (
    CuisineType,
    DishCategory,
    PriceLevel,
    RestaurantFeature,
)
from app.domains.restaurants.domain.exceptions import (
    DishNotFoundException,
    InvalidCuisineTypeException,
    InvalidPriceLevelException,
    RestaurantAlreadyExistsException,
    RestaurantNotFoundException,
)
from app.domains.restaurants.domain.interfaces import (
    DishRepositoryInterface,
    RestaurantRepositoryInterface,
)


__all__ = [
    # Entities
    "Dish",
    "DishData",
    "Restaurant",
    "RestaurantData",
    # Enums
    "CuisineType",
    "DishCategory",
    "PriceLevel",
    "RestaurantFeature",
    # Exceptions
    "DishNotFoundException",
    "RestaurantNotFoundException",
    "RestaurantAlreadyExistsException",
    "InvalidCuisineTypeException",
    "InvalidPriceLevelException",
    # Interfaces
    "DishRepositoryInterface",
    "RestaurantRepositoryInterface",
]
