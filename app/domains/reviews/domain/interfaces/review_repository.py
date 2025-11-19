"""Review repository interface.

This module defines the interface (protocol) for review repository operations.
"""

from typing import Any, Protocol

from app.domains.reviews.domain.entities import Review, ReviewData
from app.domains.reviews.domain.enums import EntityType
from app.domains.reviews.domain.value_objects import ReviewStats


class ReviewRepositoryInterface(Protocol):
    """Review repository interface.

    This interface defines the contract for review repository implementations.
    Following the Dependency Inversion Principle, the domain layer defines
    the interface, and the infrastructure layer provides the implementation.

    All methods should raise appropriate domain exceptions when operations fail.

    Unit of Work Pattern:
        This repository supports the Unit of Work pattern through the commit parameter
        and explicit commit/rollback methods. This allows grouping multiple operations
        into a single transaction.

        Example usage:
            >>> # Create multiple reviews in a single transaction
            >>> try:
            ...     review1 = await repository.create(review_data1, commit=False)
            ...     review2 = await repository.create(review_data2, commit=False)
            ...     await repository.commit()  # Commit both at once
            ... except Exception:
            ...     await repository.rollback()  # Rollback both if any fails
    """

    async def create(
        self,
        review_data: ReviewData,
        created_by: str,
        commit: bool = True,
    ) -> Review:
        """Create a new review.

        Args:
            review_data: The review data to create
            created_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            The created review with generated ID and timestamps

        Raises:
            IntegrityError: If user already reviewed this entity (duplicate constraint)
        """
        ...

    async def get_by_id(self, review_id: str) -> Review | None:
        """Get a review by its ID.

        Args:
            review_id: The ULID of the review

        Returns:
            The review if found, None otherwise
        """
        ...

    async def get_by_user_and_entity(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
    ) -> Review | None:
        """Get a review by user and entity.

        This method is used to check if a user has already reviewed an entity,
        which is critical for enforcing the "one review per user per entity" constraint.

        Args:
            user_id: The ULID of the user
            entity_type: The type of entity
            entity_id: The ULID of the entity

        Returns:
            The review if found, None otherwise
        """
        ...

    async def find(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Review]:
        """Find reviews with dynamic filters and pagination.

        This method allows querying reviews with any combination of filters
        by dynamically building the WHERE clause using model attributes.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match ReviewModel attribute names.
                    Common filters:
                    - entity_type: Type of entity (restaurant, event, place, etc.)
                    - entity_id: ULID of the entity
                    - user_id: ULID of the user
                    - status: Review status (pending, approved, rejected)
                    - rating: Exact rating (1-5)
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reviews matching the filters

        Examples:
            >>> # Get all approved reviews for a restaurant
            >>> find(
            ...     filters={
            ...         "entity_type": "restaurant",
            ...         "entity_id": "xxx",
            ...         "status": "approved",
            ...     }
            ... )

            >>> # Get all reviews by a user
            >>> find(filters={"user_id": "xxx"})

            >>> # Get 5-star reviews for a restaurant
            >>> find(
            ...     filters={
            ...         "entity_type": "restaurant",
            ...         "entity_id": "xxx",
            ...         "rating": 5,
            ...     }
            ... )
        """
        ...

    async def update(
        self,
        review_id: str,
        review_data: ReviewData,
        updated_by: str,
        commit: bool = True,
    ) -> Review | None:
        """Update an existing review.

        Args:
            review_id: The ULID of the review to update
            review_data: The updated review data
            updated_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            The updated review if found, None otherwise
        """
        ...

    async def delete(
        self,
        review_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete a review (soft delete).

        Args:
            review_id: The ULID of the review to delete
            deleted_by: User identifier for audit trail
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        ...

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count reviews with dynamic filters.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match ReviewModel attribute names.
                    Same filters as find() method.

        Returns:
            Count of reviews matching the filters

        Examples:
            >>> # Count all approved reviews for a restaurant
            >>> count(
            ...     filters={
            ...         "entity_type": "restaurant",
            ...         "entity_id": "xxx",
            ...         "status": "approved",
            ...     }
            ... )

            >>> # Count all reviews by a user
            >>> count(filters={"user_id": "xxx"})
        """
        ...

    async def find_with_count(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Review], int]:
        """Find reviews with filters and pagination, including total count.

        This method returns both the paginated results and the total count
        in a single operation, ensuring consistency between the two queries.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match ReviewModel attribute names.
                    Same filters as find() and count() methods.
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            Tuple of (list of reviews, total count)

        Examples:
            >>> # Get all approved reviews for a restaurant with pagination
            >>> reviews, total = find_with_count(
            ...     filters={
            ...         "entity_type": "restaurant",
            ...         "entity_id": "xxx",
            ...         "status": "approved",
            ...     },
            ...     offset=0,
            ...     limit=20,
            ... )

            >>> # Get all reviews by a user with pagination
            >>> reviews, total = find_with_count(
            ...     filters={"user_id": "xxx"}, offset=0, limit=10
            ... )
        """
        ...

    async def get_stats_by_entity(
        self,
        entity_type: EntityType,
        entity_id: str,
    ) -> ReviewStats:
        """Get aggregated statistics for an entity's reviews.

        This method performs complex aggregations (average rating, rating distribution,
        total count) that cannot be efficiently done with simple filtering.

        Args:
            entity_type: The type of entity
            entity_id: The ULID of the entity

        Returns:
            Aggregated review statistics including average rating and distribution
        """
        ...

    async def exists_by_user_and_entity(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
    ) -> bool:
        """Check if a user has already reviewed an entity.

        This method is optimized for existence checks and is faster than
        using get_by_user_and_entity() when you only need to know if a review exists.

        Args:
            user_id: The ULID of the user
            entity_type: The type of entity
            entity_id: The ULID of the entity

        Returns:
            True if review exists, False otherwise
        """
        ...

    async def commit(self) -> None:
        """Commit the current transaction.

        Useful for Unit of Work pattern when commit=False is used in operations.
        """
        ...

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Useful for Unit of Work pattern when an error occurs.
        """
        ...
