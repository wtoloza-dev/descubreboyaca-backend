"""Integration tests for RestaurantService list operations.

This module tests the find and count methods with focus on:
- Listing restaurants without filters
- Filtering by city and other criteria
- Pagination (offset/limit)
- Counting restaurants with filters
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.repositories import SQLiteArchiveRepository
from app.domains.restaurants.repositories import SQLiteRestaurantRepository
from app.domains.restaurants.services import RestaurantService


class TestRestaurantServiceList:
    """Integration tests for RestaurantService list operations."""

    @pytest.mark.asyncio
    async def test_find_restaurants_no_filters(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test listing all restaurants without filters.

        Given: Multiple restaurants exist in database
        When: Calling service.find_restaurants() without filters
        Then: Returns all restaurants
        """
        # Arrange
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        await create_test_restaurant(name="Restaurant 1", city="Tunja")
        await create_test_restaurant(name="Restaurant 2", city="Sogamoso")
        await create_test_restaurant(name="Restaurant 3", city="Duitama")

        # Act
        results, total = await service.find_restaurants(
            filters=None, offset=0, limit=10
        )

        # Assert
        assert len(results) == 3
        assert total == 3
        names = [r.name for r in results]
        assert "Restaurant 1" in names
        assert "Restaurant 2" in names
        assert "Restaurant 3" in names

    @pytest.mark.asyncio
    async def test_find_restaurants_with_city_filter(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test listing restaurants filtered by city.

        Given: Restaurants in different cities exist in database
        When: Calling service.find_restaurants() with city filter
        Then: Returns only restaurants from specified city
        """
        # Arrange
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        await create_test_restaurant(name="Tunja 1", city="Tunja")
        await create_test_restaurant(name="Tunja 2", city="Tunja")
        await create_test_restaurant(name="Sogamoso 1", city="Sogamoso")

        # Act
        results, total = await service.find_restaurants(
            filters={"city": "Tunja"}, offset=0, limit=10
        )

        # Assert
        assert len(results) == 2
        assert total == 2
        assert all(r.city == "Tunja" for r in results)

    @pytest.mark.asyncio
    async def test_find_restaurants_with_pagination(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test listing restaurants with pagination.

        Given: 10 restaurants exist in database
        When: Calling service.find_restaurants() with offset=5, limit=3
        Then: Returns 3 restaurants starting from the 6th
        """
        # Arrange
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        for i in range(10):
            await create_test_restaurant(name=f"Restaurant {i:02d}", city="Tunja")

        # Act
        results, total = await service.find_restaurants(filters=None, offset=5, limit=3)

        # Assert
        assert len(results) == 3
        assert total == 10  # Total de todos los restaurantes, no solo los devueltos

    @pytest.mark.asyncio
    async def test_count_restaurants_with_filter(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test counting restaurants with filter.

        Given: Multiple restaurants in different cities
        When: Calling service.count_restaurants() with city filter
        Then: Returns correct count for that city
        """
        # Arrange
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        await create_test_restaurant(name="Tunja 1", city="Tunja")
        await create_test_restaurant(name="Tunja 2", city="Tunja")
        await create_test_restaurant(name="Tunja 3", city="Tunja")
        await create_test_restaurant(name="Sogamoso 1", city="Sogamoso")

        # Act
        count = await service.count_restaurants(filters={"city": "Tunja"})

        # Assert
        assert count == 3
