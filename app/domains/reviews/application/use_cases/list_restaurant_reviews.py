"""Use case for listing reviews of a restaurant.

This module provides the business logic for retrieving all approved reviews
belonging to a specific restaurant with pagination.
"""

from app.domains.reviews.domain.entities import Review
from app.domains.reviews.domain.enums import EntityType, ReviewStatus
from app.domains.reviews.domain.interfaces import ReviewRepositoryInterface


class ListRestaurantReviewsUseCase:
    """Use case for getting all reviews for a specific restaurant.

    This use case retrieves approved reviews for a restaurant.
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
        restaurant_id: str,
        offset: int = 0,
        limit: int = 20,
        only_approved: bool = True,
    ) -> tuple[list[Review], int]:
        """Execute the list restaurant reviews use case.

        Args:
            restaurant_id: ULID of the restaurant
            offset: Number of records to skip
            limit: Maximum number of records to return
            only_approved: If True, only return approved reviews (default: True)

        Returns:
            Tuple of (list of reviews, total count)

        Example:
            >>> # Get approved reviews for a restaurant
            >>> reviews, total = await use_case.execute("01BX...")
            >>> # Get all reviews (including pending/rejected)
            >>> reviews, total = await use_case.execute("01BX...", only_approved=False)
        """
        # Build filters
        filters = {
            "entity_type": EntityType.RESTAURANT,
            "entity_id": restaurant_id,
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
