"""Integration tests for ReviewService list operations.

Focus on service orchestration with repository and database.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from ulid import ULID

from app.domains.reviews.domain.enums import EntityType
from app.domains.reviews.repositories.review import PostgreSQLReviewRepository
from app.domains.reviews.services import ReviewService


@pytest.mark.asyncio
async def test_list_user_reviews_empty(test_session: AsyncSession):
    """Test listing reviews when user has none.

    Given: User has no reviews
    When: Calling service.list_user_reviews()
    Then: Returns empty list and zero count
    """
    # Arrange
    repository = PostgreSQLReviewRepository(test_session)
    service = ReviewService(repository)
    user_id = str(ULID())

    # Act
    reviews, total = await service.list_user_reviews(user_id=user_id)

    # Assert
    assert reviews == []
    assert total == 0


@pytest.mark.asyncio
async def test_list_user_reviews_with_results(test_session: AsyncSession):
    """Test listing reviews with multiple results.

    Given: User has multiple reviews
    When: Calling service.list_user_reviews()
    Then: Returns all user's reviews with correct count
    """
    # Arrange
    repository = PostgreSQLReviewRepository(test_session)
    service = ReviewService(repository)
    user_id = str(ULID())

    # Create test reviews
    from app.domains.reviews.domain.entities import ReviewData

    for i in range(3):
        review_data = ReviewData(
            entity_type=EntityType.RESTAURANT,
            entity_id=str(ULID()),
            user_id=user_id,
            rating=5,
            title=f"Review {i}",
        )
        await repository.create(review_data)

    # Act
    reviews, total = await service.list_user_reviews(user_id=user_id)

    # Assert
    assert len(reviews) == 3
    assert total == 3
    assert all(review.user_id == user_id for review in reviews)


@pytest.mark.asyncio
async def test_list_user_reviews_with_pagination(test_session: AsyncSession):
    """Test listing reviews with pagination.

    Given: User has 5 reviews
    When: Calling service.list_user_reviews() with offset=2, limit=2
    Then: Returns 2 reviews (page 2) and total count of 5
    """
    # Arrange
    repository = PostgreSQLReviewRepository(test_session)
    service = ReviewService(repository)
    user_id = str(ULID())

    # Create test reviews
    from app.domains.reviews.domain.entities import ReviewData

    for i in range(5):
        review_data = ReviewData(
            entity_type=EntityType.RESTAURANT,
            entity_id=str(ULID()),
            user_id=user_id,
            rating=5,
            title=f"Review {i}",
        )
        await repository.create(review_data)

    # Act
    reviews, total = await service.list_user_reviews(
        user_id=user_id,
        offset=2,
        limit=2,
    )

    # Assert
    assert len(reviews) == 2
    assert total == 5


@pytest.mark.asyncio
async def test_list_user_reviews_only_returns_own_reviews(test_session: AsyncSession):
    """Test that users only see their own reviews.

    Given: Multiple users have reviews
    When: Calling service.list_user_reviews() for specific user
    Then: Returns only that user's reviews
    """
    # Arrange
    repository = PostgreSQLReviewRepository(test_session)
    service = ReviewService(repository)
    user_id_1 = str(ULID())
    user_id_2 = str(ULID())

    # Create reviews for different users
    from app.domains.reviews.domain.entities import ReviewData

    for user_id in [user_id_1, user_id_2]:
        for i in range(2):
            review_data = ReviewData(
                entity_type=EntityType.RESTAURANT,
                entity_id=str(ULID()),
                user_id=user_id,
                rating=5,
            )
            await repository.create(review_data)

    # Act
    reviews, total = await service.list_user_reviews(user_id=user_id_1)

    # Assert
    assert len(reviews) == 2
    assert total == 2
    assert all(review.user_id == user_id_1 for review in reviews)


@pytest.mark.asyncio
async def test_list_user_reviews_ordered_by_created_at_desc(
    test_session: AsyncSession,
):
    """Test reviews are ordered by created_at descending.

    Given: User has multiple reviews created at different times
    When: Calling service.list_user_reviews()
    Then: Returns reviews ordered by created_at (newest first)
    """
    # Arrange
    repository = PostgreSQLReviewRepository(test_session)
    service = ReviewService(repository)
    user_id = str(ULID())

    # Create reviews
    from app.domains.reviews.domain.entities import ReviewData

    created_ids = []
    for i in range(3):
        review_data = ReviewData(
            entity_type=EntityType.RESTAURANT,
            entity_id=str(ULID()),
            user_id=user_id,
            rating=5,
            title=f"Review {i}",
        )
        review = await repository.create(review_data)
        created_ids.append(review.id)

    # Act
    reviews, total = await service.list_user_reviews(user_id=user_id)

    # Assert
    assert len(reviews) == 3
    # Verify ordering (newest first - reverse order of creation)
    assert reviews[0].id == created_ids[2]
    assert reviews[1].id == created_ids[1]
    assert reviews[2].id == created_ids[0]
