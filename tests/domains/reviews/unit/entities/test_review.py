"""Unit tests for Review domain entities.

Tests pure domain logic without database or external dependencies.
Uses mocks where necessary to isolate business logic.
"""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.domains.reviews.domain.entities import Review, ReviewData
from app.domains.reviews.domain.enums import EntityType, ReviewStatus


class TestReviewData:
    """Unit tests for ReviewData value object (pure domain logic)."""

    def test_create_review_data_with_valid_minimal_data(self):
        """Test creating review data with minimal required fields.

        Given: Minimal valid review data (entity_type, entity_id, user_id, rating)
        When: Creating ReviewData instance
        Then: Instance is created successfully with defaults
        """
        # Arrange & Act
        review_data = ReviewData(
            entity_type=EntityType.RESTAURANT,
            entity_id="01K8E0Z3SRNDMSZPN91V7A64T3",
            user_id="01K8E0USER123456789ABCDEF",
            rating=5,
        )

        # Assert
        assert review_data.entity_type == EntityType.RESTAURANT
        assert review_data.entity_id == "01K8E0Z3SRNDMSZPN91V7A64T3"
        assert review_data.user_id == "01K8E0USER123456789ABCDEF"
        assert review_data.rating == 5
        # Verify defaults
        assert review_data.title is None
        assert review_data.comment is None
        assert review_data.photos == []
        assert review_data.visit_date is None
        assert review_data.status == ReviewStatus.APPROVED

    def test_create_review_data_with_complete_data(self):
        """Test creating review data with all fields populated.

        Given: Complete review data including optional fields
        When: Creating ReviewData instance
        Then: All fields are set correctly
        """
        # Arrange
        visit_date = datetime.now(UTC)

        # Act
        review_data = ReviewData(
            entity_type=EntityType.RESTAURANT,
            entity_id="01K8E0Z3SRNDMSZPN91V7A64T3",
            user_id="01K8E0USER123456789ABCDEF",
            rating=4,
            title="Great restaurant!",
            comment="The food was amazing and the service was excellent.",
            photos=["https://example.com/photo1.jpg", "https://example.com/photo2.jpg"],
            visit_date=visit_date,
            status=ReviewStatus.PENDING,
        )

        # Assert
        assert review_data.rating == 4
        assert review_data.title == "Great restaurant!"
        assert (
            review_data.comment == "The food was amazing and the service was excellent."
        )
        assert len(review_data.photos) == 2
        assert review_data.visit_date == visit_date
        assert review_data.status == ReviewStatus.PENDING

    def test_create_review_data_with_invalid_rating_too_high(self):
        """Test creating review with rating > 5 raises validation error.

        Given: Review data with rating = 6 (max is 5)
        When: Creating ReviewData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ReviewData(
                entity_type=EntityType.RESTAURANT,
                entity_id="01K8E0Z3SRNDMSZPN91V7A64T3",
                user_id="01K8E0USER123456789ABCDEF",
                rating=6,  # ❌ Max is 5
            )

        assert "rating" in str(exc_info.value)

    def test_create_review_data_with_invalid_rating_too_low(self):
        """Test creating review with rating < 1 raises validation error.

        Given: Review data with rating = 0 (min is 1)
        When: Creating ReviewData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ReviewData(
                entity_type=EntityType.RESTAURANT,
                entity_id="01K8E0Z3SRNDMSZPN91V7A64T3",
                user_id="01K8E0USER123456789ABCDEF",
                rating=0,  # ❌ Min is 1
            )

        assert "rating" in str(exc_info.value)

    def test_create_review_data_with_invalid_entity_id_too_long(self):
        """Test creating review with entity_id > 26 chars raises error.

        Given: Review data with entity_id longer than 26 characters
        When: Creating ReviewData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ReviewData(
                entity_type=EntityType.RESTAURANT,
                entity_id="01K8E0Z3SRNDMSZPN91V7A64T3TOOLONG",  # ❌ > 26 chars
                user_id="01K8E0USER123456789ABCDEF",
                rating=5,
            )

        assert "entity_id" in str(exc_info.value)

    def test_create_review_data_with_invalid_user_id_too_long(self):
        """Test creating review with user_id > 26 chars raises error.

        Given: Review data with user_id longer than 26 characters
        When: Creating ReviewData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ReviewData(
                entity_type=EntityType.RESTAURANT,
                entity_id="01K8E0Z3SRNDMSZPN91V7A64T3",
                user_id="01K8E0USER123456789ABCDEFTOOLONG",  # ❌ > 26 chars
                rating=5,
            )

        assert "user_id" in str(exc_info.value)

    def test_create_review_data_with_invalid_title_too_long(self):
        """Test creating review with title > 255 chars raises error.

        Given: Review data with title longer than 255 characters
        When: Creating ReviewData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            ReviewData(
                entity_type=EntityType.RESTAURANT,
                entity_id="01K8E0Z3SRNDMSZPN91V7A64T3",
                user_id="01K8E0USER123456789ABCDEF",
                rating=5,
                title="A" * 256,  # ❌ > 255 chars
            )

        assert "title" in str(exc_info.value)


class TestReview:
    """Unit tests for Review entity (with audit fields)."""

    def test_create_review_entity_with_all_fields(self):
        """Test creating complete Review entity with audit fields.

        Given: Complete review data including ID and timestamps
        When: Creating Review entity
        Then: All fields including audit fields are set correctly
        """
        # Arrange
        now = datetime.now(UTC)
        review_id = "01K8E0Z3SRNDMSZPN91V7A64T3"
        entity_id = "01K8E0ENTITY123456789ABCD"
        user_id = "01K8E0USER123456789ABCDEF"

        # Act
        review = Review(
            # Audit fields
            id=review_id,
            created_at=now,
            updated_at=now,
            # Review data
            entity_type=EntityType.RESTAURANT,
            entity_id=entity_id,
            user_id=user_id,
            rating=5,
            title="Excellent!",
            comment="Best restaurant ever",
            photos=["https://example.com/photo.jpg"],
            visit_date=now,
            status=ReviewStatus.APPROVED,
        )

        # Assert
        # Audit fields
        assert review.id == review_id
        assert review.created_at == now
        assert review.updated_at == now
        # Review data
        assert review.entity_type == EntityType.RESTAURANT
        assert review.entity_id == entity_id
        assert review.user_id == user_id
        assert review.rating == 5
        assert review.title == "Excellent!"
        assert review.comment == "Best restaurant ever"

    def test_review_validates_from_attributes(self):
        """Test that Review can be validated from ORM model attributes.

        Given: Dictionary with review attributes (simulating ORM)
        When: Using model_validate() with from_attributes config
        Then: Review entity is created successfully
        """
        # Arrange
        orm_data = {
            "id": "01K8E0Z3SRNDMSZPN91V7A64T3",
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC),
            "entity_type": EntityType.RESTAURANT,
            "entity_id": "01K8E0ENTITY123456789ABCD",
            "user_id": "01K8E0USER123456789ABCDEF",
            "rating": 5,
            "title": "Great!",
            "comment": "Amazing food",
            "photos": [],
            "visit_date": None,
            "status": ReviewStatus.APPROVED,
        }

        # Act
        review = Review.model_validate(orm_data)

        # Assert
        assert review.id == "01K8E0Z3SRNDMSZPN91V7A64T3"
        assert review.rating == 5
        assert review.title == "Great!"

    def test_review_model_dump_includes_all_fields(self):
        """Test that model_dump includes all review fields.

        Given: Review entity with all fields populated
        When: Calling model_dump()
        Then: All fields are included in the dictionary
        """
        # Arrange
        now = datetime.now(UTC)
        review = Review(
            id="01K8E0Z3SRNDMSZPN91V7A64T3",
            created_at=now,
            updated_at=now,
            entity_type=EntityType.RESTAURANT,
            entity_id="01K8E0ENTITY123456789ABCD",
            user_id="01K8E0USER123456789ABCDEF",
            rating=4,
            title="Good",
            comment="Nice place",
            photos=["https://example.com/photo.jpg"],
            visit_date=now,
            status=ReviewStatus.APPROVED,
        )

        # Act
        dumped = review.model_dump()

        # Assert
        assert "id" in dumped
        assert "created_at" in dumped
        assert "updated_at" in dumped
        assert "entity_type" in dumped
        assert "entity_id" in dumped
        assert "user_id" in dumped
        assert "rating" in dumped
        assert "title" in dumped
        assert "comment" in dumped
        assert "photos" in dumped
        assert "visit_date" in dumped
        assert "status" in dumped
