"""Integration tests for RestaurantRepository find operations.

This module tests the find method with focus on:
- Finding all restaurants without filters
- Filtering by various criteria (city, price_level, etc.)
- Multiple filter combinations
- Pagination (offset/limit)
- Empty results
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.repositories import RestaurantRepositorySQLite


class TestRestaurantRepositoryFind:
    """Integration tests for RestaurantRepository find operations."""

    @pytest.mark.asyncio
    async def test_find_all_no_filters(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test finding all restaurants without filters.

        Given: Multiple restaurants in database
        When: Calling repository.find() without filters
        Then: Returns all restaurants
        """
        # Arrange
        repository = RestaurantRepositorySQLite(test_session)
        await create_test_restaurant(name="Restaurant 1", city="Tunja")
        await create_test_restaurant(name="Restaurant 2", city="Sogamoso")
        await create_test_restaurant(name="Restaurant 3", city="Duitama")

        # Act
        results = await repository.find(filters=None, offset=0, limit=10)

        # Assert
        assert len(results) == 3
        names = [r.name for r in results]
        assert "Restaurant 1" in names
        assert "Restaurant 2" in names
        assert "Restaurant 3" in names

    @pytest.mark.asyncio
    async def test_find_with_city_filter(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test finding restaurants filtered by city.

        Given: Restaurants in different cities
        When: Calling repository.find() with city filter
        Then: Returns only restaurants from specified city
        """
        # Arrange
        repository = RestaurantRepositorySQLite(test_session)
        await create_test_restaurant(name="Tunja 1", city="Tunja")
        await create_test_restaurant(name="Tunja 2", city="Tunja")
        await create_test_restaurant(name="Sogamoso 1", city="Sogamoso")

        # Act
        results = await repository.find(filters={"city": "Tunja"}, offset=0, limit=10)

        # Assert
        assert len(results) == 2
        assert all(r.city == "Tunja" for r in results)
        names = [r.name for r in results]
        assert "Tunja 1" in names
        assert "Tunja 2" in names
        assert "Sogamoso 1" not in names

    @pytest.mark.asyncio
    async def test_find_with_price_level_filter(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test finding restaurants filtered by price level.

        Given: Restaurants with different price levels
        When: Calling repository.find() with price_level filter
        Then: Returns only restaurants with specified price level
        """
        # Arrange
        repository = RestaurantRepositorySQLite(test_session)
        await create_test_restaurant(name="Budget", city="Tunja", price_level=1)
        await create_test_restaurant(name="Moderate 1", city="Tunja", price_level=2)
        await create_test_restaurant(name="Moderate 2", city="Tunja", price_level=2)
        await create_test_restaurant(name="Expensive", city="Tunja", price_level=3)

        # Act
        results = await repository.find(filters={"price_level": 2}, offset=0, limit=10)

        # Assert
        assert len(results) == 2
        assert all(r.price_level == 2 for r in results)

    @pytest.mark.asyncio
    async def test_find_with_multiple_filters(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test finding restaurants with multiple filters combined.

        Given: Restaurants with various attributes
        When: Calling repository.find() with city and price_level filters
        Then: Returns only restaurants matching all filters
        """
        # Arrange
        repository = RestaurantRepositorySQLite(test_session)
        # This should match
        await create_test_restaurant(name="Match Both", city="Tunja", price_level=2)
        # These should NOT match
        await create_test_restaurant(name="Wrong City", city="Sogamoso", price_level=2)
        await create_test_restaurant(name="Wrong Price", city="Tunja", price_level=1)

        # Act
        results = await repository.find(
            filters={"city": "Tunja", "price_level": 2}, offset=0, limit=10
        )

        # Assert
        assert len(results) == 1
        assert results[0].name == "Match Both"
        assert results[0].city == "Tunja"
        assert results[0].price_level == 2

    @pytest.mark.asyncio
    async def test_find_with_pagination(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test finding restaurants with pagination.

        Given: 10 restaurants in database
        When: Calling repository.find() with offset=3, limit=2
        Then: Returns 2 restaurants starting from 4th
        """
        # Arrange
        repository = RestaurantRepositorySQLite(test_session)
        for i in range(10):
            await create_test_restaurant(name=f"Restaurant {i:02d}", city="Tunja")

        # Act
        results = await repository.find(filters=None, offset=3, limit=2)

        # Assert
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_find_empty_result(self, test_session: AsyncSession):
        """Test finding restaurants with filter that matches nothing.

        Given: Empty database
        When: Calling repository.find() with any filter
        Then: Returns empty list
        """
        # Arrange
        repository = RestaurantRepositorySQLite(test_session)

        # Act
        results = await repository.find(
            filters={"city": "NonExistent"}, offset=0, limit=10
        )

        # Assert
        assert len(results) == 0
        assert results == []
