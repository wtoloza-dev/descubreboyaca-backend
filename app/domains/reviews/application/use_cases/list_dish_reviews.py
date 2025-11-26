"""Use case for listing reviews of a dish.

This module provides the business logic for retrieving all approved reviews
belonging to a specific dish with pagination.
"""

from app.domains.reviews.domain.entities import Review
from app.domains.reviews.domain.enums import EntityType, ReviewStatus
from app.domains.reviews.domain.interfaces import ReviewRepositoryInterface


class ListDishReviewsUseCase:
    """Use case for getting all reviews for a specific dish.

    This use case retrieves approved reviews for a dish.
    Designed for public endpoints where only approved reviews should be shown.

    Attributes:
        repository: Review repository for data retrieval
    """

    def __init__(self, repository: ReviewRepositoryInterface) -> None:
        """Initialize the use case with dependencies.

        Args:
            repository: Review repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        dish_id: str,
        offset: int = 0,
        limit: int = 20,
        only_approved: bool = True,
    ) -> tuple[list[Review], int]:
        """Execute the list dish reviews use case.

        Args:
            dish_id: ULID of the dish
            offset: Number of records to skip
            limit: Maximum number of records to return
            only_approved: If True, only return approved reviews (default: True)

        Returns:
            Tuple of (list of reviews, total count)

        Example:
            >>> # Get approved reviews for a dish
            >>> reviews, total = await use_case.execute("01BX...")
            >>> # Get all reviews (including pending/rejected)
            >>> reviews, total = await use_case.execute("01BX...", only_approved=False)
        """
        # Build filters
        filters = {
            "entity_type": EntityType.DISH,
            "entity_id": dish_id,
        }

        # Add status filter if only approved reviews should be returned
        if only_approved:
            filters["status"] = ReviewStatus.APPROVED

        # Get reviews with count in single operation
        return await self.repository.find_with_count(
            filters=filters,
            offset=offset,
            limit=limit,
        )
