"""Integration tests for DishRepository find operations.

This module tests the find and get_by_restaurant_id methods of DishRepositorySQLite.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.infrastructure.persistence.repositories.dish.sqlite import (
    SQLiteDishRepository,
)


class TestDishRepositoryFind:
    """Integration tests for DishRepository find operations."""

    @pytest.mark.asyncio
    async def test_find_all(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test finding all dishes without filters.

        Given: Multiple dishes exist in database
        When: Calling repository.find() without filters
        Then: Returns all dishes
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 1")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 2")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 3")

        # Act
        result = await repository.find()

        # Assert
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_find_with_category_filter(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test finding dishes filtered by category.

        Given: Dishes in different categories exist
        When: Calling repository.find() with category filter
        Then: Returns only dishes in that category
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id, name="Appetizer", category="appetizer"
        )
        await create_test_dish(
            restaurant_id=restaurant.id, name="Dessert 1", category="dessert"
        )
        await create_test_dish(
            restaurant_id=restaurant.id, name="Dessert 2", category="dessert"
        )

        # Act
        result = await repository.find(filters={"category": "dessert"})

        # Assert
        assert len(result) == 2
        assert all(d.category == "dessert" for d in result)

    @pytest.mark.asyncio
    async def test_find_with_pagination(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test pagination with offset and limit.

        Given: 10 dishes exist
        When: Requesting with offset=3, limit=2
        Then: Returns 2 dishes starting from position 3
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        for i in range(10):
            await create_test_dish(
                restaurant_id=restaurant.id,
                name=f"Dish {i:02d}",
                display_order=i,
            )

        # Act
        result = await repository.find(offset=3, limit=2)

        # Assert
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_find_ordered_by_display_order_and_name(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test dishes are ordered by display_order, then name.

        Given: Dishes with different display orders
        When: Finding all dishes
        Then: Results sorted by display_order (asc), then name (asc)
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id, name="Zebra", display_order=2
        )
        await create_test_dish(
            restaurant_id=restaurant.id, name="Apple", display_order=1
        )
        await create_test_dish(
            restaurant_id=restaurant.id, name="Banana", display_order=1
        )

        # Act
        result = await repository.find()

        # Assert
        assert len(result) == 3
        assert result[0].name == "Apple"  # display_order=1, name=A
        assert result[1].name == "Banana"  # display_order=1, name=B
        assert result[2].name == "Zebra"  # display_order=2

    @pytest.mark.asyncio
    async def test_get_by_restaurant_id(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test getting dishes for a specific restaurant.

        Given: Two restaurants with their own dishes
        When: Calling get_by_restaurant_id() for restaurant 1
        Then: Returns only dishes from restaurant 1
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant1 = await create_test_restaurant(name="Restaurant 1")
        restaurant2 = await create_test_restaurant(name="Restaurant 2")

        await create_test_dish(restaurant_id=restaurant1.id, name="R1 Dish 1")
        await create_test_dish(restaurant_id=restaurant1.id, name="R1 Dish 2")
        await create_test_dish(restaurant_id=restaurant2.id, name="R2 Dish 1")

        # Act
        result = await repository.get_by_restaurant_id(restaurant1.id)

        # Assert
        assert len(result) == 2
        assert all(d.restaurant_id == restaurant1.id for d in result)

    @pytest.mark.asyncio
    async def test_get_by_restaurant_id_with_filters(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test filtering dishes within a specific restaurant.

        Given: A restaurant with dishes in different categories
        When: Getting restaurant dishes filtered by category
        Then: Returns only dishes matching restaurant and category
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id, name="Appetizer", category="appetizer"
        )
        await create_test_dish(
            restaurant_id=restaurant.id, name="Dessert 1", category="dessert"
        )
        await create_test_dish(
            restaurant_id=restaurant.id, name="Dessert 2", category="dessert"
        )

        # Act
        result = await repository.get_by_restaurant_id(
            restaurant.id, filters={"category": "dessert"}
        )

        # Assert
        assert len(result) == 2
        assert all(d.category == "dessert" for d in result)
        assert all(d.restaurant_id == restaurant.id for d in result)

    @pytest.mark.asyncio
    async def test_find_with_multiple_filters(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test combining multiple filters.

        Given: Dishes with various properties
        When: Filtering by category and availability
        Then: Returns only dishes matching all filters
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Available Dessert",
            category="dessert",
            is_available=True,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Unavailable Dessert",
            category="dessert",
            is_available=False,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Available Main",
            category="main_course",
            is_available=True,
        )

        # Act
        result = await repository.find(
            filters={"category": "dessert", "is_available": True}
        )

        # Assert
        assert len(result) == 1
        assert result[0].category == "dessert"
        assert result[0].is_available is True
