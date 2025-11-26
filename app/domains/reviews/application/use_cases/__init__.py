"""Review application use cases.

This package contains all use cases for the review domain.
Each use case represents a single business operation following the
Single Responsibility Principle.

Architecture:
    - Each use case has a single `execute()` method
    - Dependencies are injected via constructor
    - Business logic is isolated and testable
    - No framework dependencies (FastAPI, SQLAlchemy)
"""

from .list_dish_reviews import ListDishReviewsUseCase
from .list_restaurant_reviews import ListRestaurantReviewsUseCase


__all__ = [
    "ListRestaurantReviewsUseCase",
    "ListDishReviewsUseCase",
]
