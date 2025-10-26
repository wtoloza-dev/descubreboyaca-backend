"""Dish repository implementations.

This package contains concrete implementations of the dish repository interface.
"""

from .postgresql import DishRepositoryPostgreSQL
from .sqlite import DishRepositorySQLite


__all__ = [
    "DishRepositoryPostgreSQL",
    "DishRepositorySQLite",
]

