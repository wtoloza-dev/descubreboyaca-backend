"""Dish repository implementations.

This package contains concrete implementations of the dish repository interface.
"""

from .postgresql import PostgreSQLDishRepository
from .sqlite import SQLiteDishRepository


__all__ = [
    "SQLiteDishRepository",
    "PostgreSQLDishRepository",
]
