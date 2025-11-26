"""Review domain dependencies.

This module provides async dependency functions for the reviews domain.
"""

from .review import (
    get_review_repository_dependency,
    get_review_service_dependency,
)
from .use_cases import (
    get_list_dish_reviews_use_case_dependency,
    get_list_restaurant_reviews_use_case_dependency,
)


__all__ = [
    "get_review_repository_dependency",
    "get_review_service_dependency",
    "get_list_restaurant_reviews_use_case_dependency",
    "get_list_dish_reviews_use_case_dependency",
]
