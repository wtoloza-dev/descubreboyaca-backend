"""Review service implementation.

This module implements the review service for business logic orchestration.
"""

from app.domains.reviews.domain.entities import Review
from app.domains.reviews.domain.enums import EntityType, ReviewStatus
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

        # Get reviews and total count in single operation
        return await self.repository.find_with_count(
            filters=filters,
            offset=offset,
            limit=limit,
        )

    async def list_entity_reviews(
        self,
        entity_type: EntityType,
        entity_id: str,
        offset: int = 0,
        limit: int = 20,
        only_approved: bool = True,
    ) -> tuple[list[Review], int]:
        """List reviews for a specific entity (restaurant, dish, etc.).

        Args:
            entity_type: Type of entity (restaurant, dish, event, etc.)
            entity_id: ULID of the entity
            offset: Number of records to skip
            limit: Maximum number of records to return
            only_approved: If True, only return approved reviews (default: True)

        Returns:
            Tuple of (list of reviews, total count)

        Example:
            >>> # Get approved reviews for a restaurant
            >>> reviews, total = await service.list_entity_reviews(
            ...     EntityType.RESTAURANT,
            ...     "01BX...",
            ... )

        """
        # Build filters
        filters = {
            "entity_type": entity_type.value,
            "entity_id": entity_id,
        }

        # Add status filter if only approved reviews should be returned
        if only_approved:
            filters["status"] = ReviewStatus.APPROVED.value

        # Get reviews and total count in single operation
        return await self.repository.find_with_count(
            filters=filters,
            offset=offset,
            limit=limit,
        )
