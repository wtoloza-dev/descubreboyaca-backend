"""Unit tests for Pagination domain entity.

Tests pure domain logic without database or external dependencies.
"""

import pytest
from pydantic import ValidationError

from app.shared.domain.entities import Pagination


class TestPagination:
    """Unit tests for Pagination entity."""

    def test_create_pagination_with_valid_data(self):
        """Test creating pagination with valid data.

        Given: Valid page and page_size
        When: Creating Pagination instance
        Then: Instance is created with correct offset and limit calculated
        """
        # Arrange & Act
        pagination = Pagination(page=1, page_size=20)

        # Assert
        assert pagination.page == 1
        assert pagination.page_size == 20
        assert pagination.offset == 0
        assert pagination.limit == 20

    def test_pagination_calculates_offset_correctly_page_2(self):
        """Test offset calculation for page 2.

        Given: Page 2 with page_size 20
        When: Creating Pagination instance
        Then: Offset is calculated as 20 (skip first 20 records)
        """
        # Arrange & Act
        pagination = Pagination(page=2, page_size=20)

        # Assert
        assert pagination.offset == 20
        assert pagination.limit == 20

    def test_pagination_calculates_offset_correctly_page_3(self):
        """Test offset calculation for page 3.

        Given: Page 3 with page_size 10
        When: Creating Pagination instance
        Then: Offset is calculated as 20 (skip first 20 records)
        """
        # Arrange & Act
        pagination = Pagination(page=3, page_size=10)

        # Assert
        assert pagination.offset == 20
        assert pagination.limit == 10

    def test_pagination_with_different_page_sizes(self):
        """Test pagination with various page sizes.

        Given: Different page sizes
        When: Creating Pagination instances
        Then: Offset is calculated correctly for each
        """
        # Arrange & Act & Assert
        # Page 1, page_size 10
        p1 = Pagination(page=1, page_size=10)
        assert p1.offset == 0
        assert p1.limit == 10

        # Page 5, page_size 25
        p2 = Pagination(page=5, page_size=25)
        assert p2.offset == 100  # (5-1) * 25 = 100
        assert p2.limit == 25

        # Page 10, page_size 50
        p3 = Pagination(page=10, page_size=50)
        assert p3.offset == 450  # (10-1) * 50 = 450
        assert p3.limit == 50

    def test_pagination_with_page_zero_raises_error(self):
        """Test creating pagination with page 0 raises validation error.

        Given: Page 0 (invalid, should be >= 1)
        When: Creating Pagination instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Pagination(page=0, page_size=20)  # ❌ Page must be >= 1

        assert "page" in str(exc_info.value)

    def test_pagination_with_negative_page_raises_error(self):
        """Test creating pagination with negative page raises error.

        Given: Negative page number
        When: Creating Pagination instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Pagination(page=-1, page_size=20)  # ❌ Page must be >= 1

        assert "page" in str(exc_info.value)

    def test_pagination_with_page_size_zero_raises_error(self):
        """Test creating pagination with page_size 0 raises error.

        Given: Page_size 0 (invalid, should be >= 1)
        When: Creating Pagination instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Pagination(page=1, page_size=0)  # ❌ Page_size must be >= 1

        assert "page_size" in str(exc_info.value)

    def test_pagination_with_page_size_over_100_raises_error(self):
        """Test creating pagination with page_size > 100 raises error.

        Given: Page_size 101 (invalid, max is 100)
        When: Creating Pagination instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Pagination(page=1, page_size=101)  # ❌ Max page_size is 100

        assert "page_size" in str(exc_info.value)

    def test_pagination_is_immutable(self):
        """Test that Pagination is immutable (frozen).

        Given: Created Pagination instance
        When: Attempting to modify attributes
        Then: Raises ValidationError or AttributeError
        """
        # Arrange
        pagination = Pagination(page=1, page_size=20)

        # Act & Assert
        with pytest.raises((ValidationError, AttributeError)):
            pagination.page = 2  # type: ignore[misc]

    def test_pagination_limit_equals_page_size(self):
        """Test that limit property equals page_size.

        Given: Pagination with specific page_size
        When: Accessing limit property
        Then: Returns same value as page_size
        """
        # Arrange & Act
        pagination = Pagination(page=1, page_size=50)

        # Assert
        assert pagination.limit == pagination.page_size
        assert pagination.limit == 50

    def test_pagination_max_valid_page_size(self):
        """Test pagination with maximum valid page_size.

        Given: Page_size 100 (maximum allowed)
        When: Creating Pagination instance
        Then: Instance is created successfully
        """
        # Arrange & Act
        pagination = Pagination(page=1, page_size=100)

        # Assert
        assert pagination.page_size == 100
        assert pagination.limit == 100
        assert pagination.offset == 0

    def test_pagination_min_valid_page_size(self):
        """Test pagination with minimum valid page_size.

        Given: Page_size 1 (minimum allowed)
        When: Creating Pagination instance
        Then: Instance is created successfully
        """
        # Arrange & Act
        pagination = Pagination(page=5, page_size=1)

        # Assert
        assert pagination.page_size == 1
        assert pagination.limit == 1
        assert pagination.offset == 4  # (5-1) * 1 = 4
