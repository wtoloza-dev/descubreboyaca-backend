"""Integration tests for DishRepository count operations.

This module tests the count and count_by_restaurant_id methods of DishRepositorySQLite.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.repositories.dish.sqlite import DishRepositorySQLite


class TestDishRepositoryCount:
    """Integration tests for DishRepository count operations."""

    @pytest.mark.asyncio
    async def test_count_all(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test counting all dishes without filters.

        Given: Multiple dishes exist
        When: Calling repository.count() without filters
        Then: Returns total count of all dishes
        """
        # Arrange
        repository = DishRepositorySQLite(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 1")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 2")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 3")

        # Act
        result = await repository.count()

        # Assert
        assert result == 3

    @pytest.mark.asyncio
    async def test_count_empty(self, test_session: AsyncSession):
        """Test counting when no dishes exist.

        Given: No dishes in database
        When: Calling repository.count()
        Then: Returns 0
        """
        # Arrange
        repository = DishRepositorySQLite(test_session)

        # Act
        result = await repository.count()

        # Assert
        assert result == 0

    @pytest.mark.asyncio
    async def test_count_with_filter(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test counting dishes with filter applied.

        Given: Dishes in different categories exist
        When: Counting with category filter
        Then: Returns count of dishes in that category
        """
        # Arrange
        repository = DishRepositorySQLite(test_session)
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
        result = await repository.count(filters={"category": "dessert"})

        # Assert
        assert result == 2

    @pytest.mark.asyncio
    async def test_count_by_restaurant_id(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test counting dishes for a specific restaurant.

        Given: Two restaurants with their own dishes
        When: Counting dishes for restaurant 1
        Then: Returns count of only restaurant 1 dishes
        """
        # Arrange
        repository = DishRepositorySQLite(test_session)
        restaurant1 = await create_test_restaurant(name="Restaurant 1")
        restaurant2 = await create_test_restaurant(name="Restaurant 2")

        await create_test_dish(restaurant_id=restaurant1.id, name="R1 Dish 1")
        await create_test_dish(restaurant_id=restaurant1.id, name="R1 Dish 2")
        await create_test_dish(restaurant_id=restaurant2.id, name="R2 Dish 1")

        # Act
        result = await repository.count_by_restaurant_id(restaurant1.id)

        # Assert
        assert result == 2

    @pytest.mark.asyncio
    async def test_count_by_restaurant_id_with_filter(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test counting restaurant dishes with additional filter.

        Given: A restaurant with dishes in different categories
        When: Counting with restaurant ID and category filter
        Then: Returns count matching both criteria
        """
        # Arrange
        repository = DishRepositorySQLite(test_session)
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
        result = await repository.count_by_restaurant_id(
            restaurant.id, filters={"category": "dessert"}
        )

        # Assert
        assert result == 2

    @pytest.mark.asyncio
    async def test_count_with_multiple_filters(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test counting with multiple combined filters.

        Given: Dishes with various properties
        When: Counting with category and availability filters
        Then: Returns count of dishes matching all filters
        """
        # Arrange
        repository = DishRepositorySQLite(test_session)
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
        result = await repository.count(
            filters={"category": "dessert", "is_available": True}
        )

        # Assert
        assert result == 1
