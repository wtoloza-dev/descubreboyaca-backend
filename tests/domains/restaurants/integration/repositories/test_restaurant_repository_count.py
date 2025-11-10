"""Integration tests for RestaurantRepository count operations.

This module tests the count method with focus on:
- Counting all restaurants
- Counting with filters (city, price_level, etc.)
- Multiple filter combinations
- Empty database handling
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.infrastructure.persistence.repositories import (
    SQLiteRestaurantRepository,
)


class TestRestaurantRepositoryCount:
    """Integration tests for RestaurantRepository count operations."""

    @pytest.mark.asyncio
    async def test_count_all_restaurants(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test counting all restaurants without filters.

        Given: Multiple restaurants in database
        When: Calling repository.count() without filters
        Then: Returns total count
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        await create_test_restaurant(name="Restaurant 1")
        await create_test_restaurant(name="Restaurant 2")
        await create_test_restaurant(name="Restaurant 3")

        # Act
        count = await repository.count(filters=None)

        # Assert
        assert count == 3

    @pytest.mark.asyncio
    async def test_count_with_city_filter(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test counting restaurants filtered by city.

        Given: Restaurants in different cities
        When: Calling repository.count() with city filter
        Then: Returns count for specified city only
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        await create_test_restaurant(name="Tunja 1", city="Tunja")
        await create_test_restaurant(name="Tunja 2", city="Tunja")
        await create_test_restaurant(name="Tunja 3", city="Tunja")
        await create_test_restaurant(name="Sogamoso 1", city="Sogamoso")

        # Act
        count = await repository.count(filters={"city": "Tunja"})

        # Assert
        assert count == 3

    @pytest.mark.asyncio
    async def test_count_with_multiple_filters(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test counting restaurants with multiple filters.

        Given: Restaurants with various attributes
        When: Calling repository.count() with multiple filters
        Then: Returns count matching all filters
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        await create_test_restaurant(name="Match 1", city="Tunja", price_level=2)
        await create_test_restaurant(name="Match 2", city="Tunja", price_level=2)
        await create_test_restaurant(name="No Match", city="Tunja", price_level=1)
        await create_test_restaurant(name="No Match 2", city="Sogamoso", price_level=2)

        # Act
        count = await repository.count(filters={"city": "Tunja", "price_level": 2})

        # Assert
        assert count == 2

    @pytest.mark.asyncio
    async def test_count_empty_database(self, test_session: AsyncSession):
        """Test counting in empty database.

        Given: Empty database
        When: Calling repository.count()
        Then: Returns 0
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)

        # Act
        count = await repository.count(filters=None)

        # Assert
        assert count == 0
