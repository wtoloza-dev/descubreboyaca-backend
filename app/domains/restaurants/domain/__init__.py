"""Restaurants domain layer.

This package contains domain primitives and building blocks for the restaurants
bounded context: entities, value objects, enums, and constants.
"""

from app.domains.restaurants.domain.entities import Restaurant, RestaurantData
from app.domains.restaurants.domain.enums import (
    CuisineType,
    PriceLevel,
    RestaurantFeature,
)
from app.domains.restaurants.domain.exceptions import (
    InvalidCuisineTypeException,
    InvalidPriceLevelException,
    RestaurantAlreadyExistsException,
    RestaurantNotFoundException,
)
from app.domains.restaurants.domain.interfaces import (
    RestaurantRepositoryInterface,
)


__all__ = [
    # Entities
    "Restaurant",
    "RestaurantData",
    # Enums
    "CuisineType",
    "PriceLevel",
    "RestaurantFeature",
    # Exceptions
    "RestaurantNotFoundException",
    "RestaurantAlreadyExistsException",
    "InvalidCuisineTypeException",
    "InvalidPriceLevelException",
    # Interfaces
    "RestaurantRepositoryInterface",
]
