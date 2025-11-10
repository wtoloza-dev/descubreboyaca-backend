"""Integration tests for DishService list operations.

This module tests the get_restaurant_dishes method of DishService.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.infrastructure.persistence.repositories import (
    SQLiteArchiveRepository,
)
from app.domains.restaurants.application.services.dish import DishService
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.infrastructure.persistence.repositories.dish.sqlite import (
    SQLiteDishRepository,
)
from app.domains.restaurants.infrastructure.persistence.repositories.restaurant.sqlite import (
    SQLiteRestaurantRepository,
)
from app.shared.domain.factories import generate_ulid


class TestDishServiceList:
    """Integration tests for DishService list operations."""

    @pytest.mark.asyncio
    async def test_get_restaurant_dishes_with_results(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test getting dishes for a restaurant returns list and count.

        Given: A restaurant with multiple dishes exists
        When: Calling service.get_restaurant_dishes()
        Then: Returns list of dishes and correct total count
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 1")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 2")
        await create_test_dish(restaurant_id=restaurant.id, name="Dish 3")

        # Act
        dishes, total = await service.get_restaurant_dishes(restaurant.id)

        # Assert
        assert len(dishes) == 3
        assert total == 3
        assert all(d.restaurant_id == restaurant.id for d in dishes)

    @pytest.mark.asyncio
    async def test_get_restaurant_dishes_empty(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
    ):
        """Test getting dishes for restaurant with no dishes returns empty list.

        Given: A restaurant exists with no dishes
        When: Calling service.get_restaurant_dishes()
        Then: Returns empty list and count of 0
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        restaurant = await create_test_restaurant(name="Empty Restaurant")

        # Act
        dishes, total = await service.get_restaurant_dishes(restaurant.id)

        # Assert
        assert dishes == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_get_restaurant_dishes_nonexistent_restaurant(
        self, test_session: AsyncSession
    ):
        """Test getting dishes for non-existent restaurant raises exception.

        Given: Restaurant ID that doesn't exist
        When: Calling service.get_restaurant_dishes()
        Then: Raises RestaurantNotFoundException
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        nonexistent_id = generate_ulid()

        # Act & Assert
        with pytest.raises(RestaurantNotFoundException) as exc_info:
            await service.get_restaurant_dishes(nonexistent_id)

        assert nonexistent_id in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_restaurant_dishes_with_pagination(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test pagination parameters are applied correctly.

        Given: A restaurant with 10 dishes
        When: Requesting with offset=3, limit=2
        Then: Returns 2 dishes starting from position 3
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        restaurant = await create_test_restaurant(name="Test Restaurant")
        for i in range(10):
            await create_test_dish(
                restaurant_id=restaurant.id,
                name=f"Dish {i:02d}",
                display_order=i,
            )

        # Act
        dishes, total = await service.get_restaurant_dishes(
            restaurant.id, offset=3, limit=2
        )

        # Assert
        assert len(dishes) == 2
        assert total == 10  # Total count should be all dishes

    @pytest.mark.asyncio
    async def test_get_restaurant_dishes_with_category_filter(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test filtering dishes by category.

        Given: A restaurant with dishes in different categories
        When: Filtering by category=dessert
        Then: Returns only dessert dishes
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

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
        dishes, total = await service.get_restaurant_dishes(
            restaurant.id, filters={"category": "dessert"}
        )

        # Assert
        assert len(dishes) == 2
        assert total == 2
        assert all(d.category == "dessert" for d in dishes)

    @pytest.mark.asyncio
    async def test_get_restaurant_dishes_with_availability_filter(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test filtering dishes by availability.

        Given: A restaurant with available and unavailable dishes
        When: Filtering by is_available=True
        Then: Returns only available dishes
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id, name="Available 1", is_available=True
        )
        await create_test_dish(
            restaurant_id=restaurant.id, name="Available 2", is_available=True
        )
        await create_test_dish(
            restaurant_id=restaurant.id, name="Unavailable", is_available=False
        )

        # Act
        dishes, total = await service.get_restaurant_dishes(
            restaurant.id, filters={"is_available": True}
        )

        # Assert
        assert len(dishes) == 2
        assert total == 2
        assert all(d.is_available is True for d in dishes)

    @pytest.mark.asyncio
    async def test_get_restaurant_dishes_with_multiple_filters(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test combining multiple filters.

        Given: A restaurant with various dishes
        When: Filtering by category and availability
        Then: Returns only dishes matching all filters
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

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
        dishes, total = await service.get_restaurant_dishes(
            restaurant.id, filters={"category": "dessert", "is_available": True}
        )

        # Assert
        assert len(dishes) == 1
        assert total == 1
        assert dishes[0].category == "dessert"
        assert dishes[0].is_available is True
