"""Review repository PostgreSQL implementation.

This module implements the review repository for PostgreSQL database operations.
"""

from decimal import Decimal
from typing import Any

from sqlmodel import and_, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.reviews.domain.entities import Review, ReviewData
from app.domains.reviews.domain.enums import EntityType, ReviewStatus
from app.domains.reviews.domain.value_objects import ReviewStats
from app.domains.reviews.models import ReviewModel


class ReviewRepositoryPostgreSQL:
    """PostgreSQL repository for review database operations.

    This repository implements the ReviewRepositoryInterface and provides
    concrete database operations using SQLModel/SQLAlchemy with async support.

    Attributes:
        session: Async SQLModel database session
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.

        Args:
            session: Async SQLModel database session
        """
        self.session = session

    async def create(self, review_data: ReviewData, commit: bool = True) -> Review:
        """Create a new review.

        The Review entity generates its own ID and timestamps following DDD
        principles. The repository only persists the entity to the database.

        Args:
            review_data: Data for the new review (without ID and timestamps)
            commit: Whether to commit the transaction immediately

        Returns:
            The created review entity with generated ID and timestamps

        Raises:
            IntegrityError: If the user has already reviewed this entity
                           (duplicate constraint violation)
        """
        # Create entity with auto-generated ID and timestamps
        review = Review(**review_data.model_dump())

        # Convert to ORM model
        model = ReviewModel.model_validate(review)

        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return review

    async def get_by_id(self, review_id: str) -> Review | None:
        """Get a review by its ID.

        Args:
            review_id: The ULID of the review

        Returns:
            The review if found, None otherwise
        """
        statement = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return None

        return Review.model_validate(model)

    async def get_by_user_and_entity(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
    ) -> Review | None:
        """Get a review by user and entity.

        Args:
            user_id: The ULID of the user
            entity_type: The type of entity
            entity_id: The ULID of the entity

        Returns:
            The review if found, None otherwise
        """
        statement = select(ReviewModel).where(
            and_(
                ReviewModel.user_id == user_id,
                ReviewModel.entity_type == entity_type,
                ReviewModel.entity_id == entity_id,
            )
        )
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return None

        return Review.model_validate(model)

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
                    Example: {"entity_type": "restaurant", "status": "approved"}
            offset: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of reviews matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute
        """
        statement = select(ReviewModel)

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(ReviewModel, field_name):
                    raise AttributeError(f"ReviewModel has no attribute '{field_name}'")

                model_field = getattr(ReviewModel, field_name)
                statement = statement.where(model_field == value)

        # Apply ordering and pagination
        statement = (
            statement.order_by(ReviewModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        # Execute query
        result = await self.session.exec(statement)
        models = result.all()

        # Convert to domain entities
        reviews = [Review.model_validate(model) for model in models]

        return reviews

    async def update(
        self, review_id: str, review_data: ReviewData, commit: bool = True
    ) -> Review | None:
        """Update an existing review.

        Args:
            review_id: The ULID of the review to update
            review_data: The updated review data
            commit: Whether to commit the transaction immediately

        Returns:
            The updated review if found, None otherwise
        """
        # Get existing review
        statement = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return None

        # Update fields
        update_data = review_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(model, key, value)

        # Update timestamp
        from datetime import UTC, datetime

        model.updated_at = datetime.now(UTC)

        self.session.add(model)

        if commit:
            await self.session.commit()
            await self.session.refresh(model)

        return Review.model_validate(model)

    async def delete(self, review_id: str, commit: bool = True) -> bool:
        """Delete a review.

        Args:
            review_id: The ULID of the review to delete
            commit: Whether to commit the transaction immediately

        Returns:
            True if deleted, False if not found
        """
        statement = select(ReviewModel).where(ReviewModel.id == review_id)
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            return False

        await self.session.delete(model)

        if commit:
            await self.session.commit()

        return True

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count reviews with dynamic filters.

        Args:
            filters: Dictionary of field names and their values to filter by.
                    Keys should match ReviewModel attribute names.
                    Same filters as find() method.

        Returns:
            Count of reviews matching the filters

        Raises:
            AttributeError: If a filter key doesn't match any model attribute
        """
        statement = select(func.count(ReviewModel.id))

        # Apply dynamic filters if provided
        if filters:
            for field_name, value in filters.items():
                # Get the model attribute dynamically
                if not hasattr(ReviewModel, field_name):
                    raise AttributeError(f"ReviewModel has no attribute '{field_name}'")

                model_field = getattr(ReviewModel, field_name)
                statement = statement.where(model_field == value)

        # Execute query
        result = await self.session.exec(statement)
        return result.one()

    async def get_stats_by_entity(
        self,
        entity_type: EntityType,
        entity_id: str,
    ) -> ReviewStats:
        """Get aggregated statistics for an entity's reviews.

        Args:
            entity_type: The type of entity
            entity_id: The ULID of the entity

        Returns:
            Aggregated review statistics
        """
        # Get rating distribution
        distribution_statement = (
            select(
                ReviewModel.rating,
                func.count(ReviewModel.id).label("count"),
            )
            .where(
                and_(
                    ReviewModel.entity_type == entity_type,
                    ReviewModel.entity_id == entity_id,
                    ReviewModel.status == ReviewStatus.APPROVED,
                )
            )
            .group_by(ReviewModel.rating)
        )

        # Execute distribution query
        distribution_result = await self.session.exec(distribution_statement)
        distribution_rows = distribution_result.all()

        # Build rating distribution dict
        rating_distribution = {i: 0 for i in range(1, 6)}
        total_reviews = 0

        for row in distribution_rows:
            rating_distribution[row[0]] = row[1]
            total_reviews += row[1]

        # Calculate average
        if total_reviews > 0:
            total_rating = sum(
                rating * count for rating, count in rating_distribution.items()
            )
            average_rating = Decimal(str(total_rating / total_reviews)).quantize(
                Decimal("0.01")
            )
        else:
            average_rating = Decimal("0.00")

        return ReviewStats(
            total_reviews=total_reviews,
            average_rating=average_rating,
            rating_distribution=rating_distribution,
        )

    async def exists_by_user_and_entity(
        self,
        user_id: str,
        entity_type: EntityType,
        entity_id: str,
    ) -> bool:
        """Check if a user has already reviewed an entity.

        Args:
            user_id: The ULID of the user
            entity_type: The type of entity
            entity_id: The ULID of the entity

        Returns:
            True if review exists, False otherwise
        """
        statement = select(func.count(ReviewModel.id)).where(
            and_(
                ReviewModel.user_id == user_id,
                ReviewModel.entity_type == entity_type,
                ReviewModel.entity_id == entity_id,
            )
        )
        result = await self.session.exec(statement)
        count = result.one()
        return count > 0

    async def commit(self) -> None:
        """Commit the current transaction.

        Useful for Unit of Work pattern when commit=False is used in operations.
        """
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction.

        Useful for Unit of Work pattern when an error occurs.
        """
        await self.session.rollback()
