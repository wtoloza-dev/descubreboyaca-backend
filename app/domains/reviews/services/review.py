"""Review service implementation.

This module implements the review service for business logic orchestration.
"""

import asyncio

from app.domains.reviews.domain.entities import Review
from app.domains.reviews.domain.interfaces import ReviewRepositoryInterface


class ReviewService:
    """Service for review business logic.

    This service orchestrates review-related use cases and coordinates
    repository operations. It contains the application's business logic
    for reviews.

    Following the architecture, application services do NOT need abstraction
    (no interface required) as they ARE the business logic.

    Attributes:
        repository: Review repository for data access
    """

    def __init__(self, repository: ReviewRepositoryInterface) -> None:
        """Initialize the service.

        Args:
            repository: Review repository implementation
        """
        self.repository = repository

    async def list_user_reviews(
        self,
        user_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Review], int]:
        """List reviews created by a specific user.

        Args:
            user_id: ULID of the user
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of reviews, total count)

        Example:
            >>> # Get all reviews by user with pagination
            >>> reviews, total = await service.list_user_reviews("01BX...")

        """
        # Build filters
        filters = {"user_id": user_id}

        # Get reviews and total count in parallel
        reviews, total = await asyncio.gather(
            self.repository.find(
                filters=filters,
                offset=offset,
                limit=limit,
            ),
            self.repository.count(filters=filters),
        )

        return reviews, total
