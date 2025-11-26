"""Review use cases dependencies.

This module provides dependency injection factories for all review-related
use cases.
"""

from typing import Annotated

from fastapi import Depends

from app.domains.reviews.application.use_cases import (
    ListDishReviewsUseCase,
    ListRestaurantReviewsUseCase,
)
from app.domains.reviews.domain.interfaces import ReviewRepositoryInterface
from app.domains.reviews.infrastructure.dependencies.review import (
    get_review_repository_dependency,
)


def get_list_restaurant_reviews_use_case_dependency(
    repository: Annotated[
        ReviewRepositoryInterface, Depends(get_review_repository_dependency)
    ],
) -> ListRestaurantReviewsUseCase:
    """Factory to create a ListRestaurantReviewsUseCase instance.

    Args:
        repository: Review repository (injected via Depends)

    Returns:
        ListRestaurantReviewsUseCase: Configured use case instance
    """
    return ListRestaurantReviewsUseCase(repository)


def get_list_dish_reviews_use_case_dependency(
    repository: Annotated[
        ReviewRepositoryInterface, Depends(get_review_repository_dependency)
    ],
) -> ListDishReviewsUseCase:
    """Factory to create a ListDishReviewsUseCase instance.

    Args:
        repository: Review repository (injected via Depends)

    Returns:
        ListDishReviewsUseCase: Configured use case instance
    """
    return ListDishReviewsUseCase(repository)
