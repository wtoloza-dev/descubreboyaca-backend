"""Integration tests for DishService find operations.

This module tests the find_dish_by_id method of DishService.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.infrastructure.persistence.repositories import (
    SQLiteArchiveRepository,
)
from app.domains.restaurants.application.services.dish import DishService
from app.domains.restaurants.domain.exceptions import DishNotFoundException
from app.domains.restaurants.infrastructure.persistence.repositories.dish.sqlite import (
    SQLiteDishRepository,
)
from app.domains.restaurants.infrastructure.persistence.repositories.restaurant.sqlite import (
    SQLiteRestaurantRepository,
)
from app.shared.domain.factories import generate_ulid


class TestDishServiceGet:
    """Integration tests for DishService find operations."""

    @pytest.mark.asyncio
    async def test_find_dish_by_id_existing(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test finding an existing dish through service.

        Given: A dish exists in database
        When: Calling service.find_dish_by_id()
        Then: Returns dish entity with correct data
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        restaurant = await create_test_restaurant(name="Test Restaurant")
        created_dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Ajiaco Santafereño",
        )

        # Act
        result = await service.find_dish_by_id(created_dish.id)

        # Assert
        assert result.id == created_dish.id
        assert result.name == "Ajiaco Santafereño"
        assert result.restaurant_id == restaurant.id

    @pytest.mark.asyncio
    async def test_find_dish_by_id_not_found(self, test_session: AsyncSession):
        """Test finding non-existent dish raises DishNotFoundException.

        Given: Dish ID that doesn't exist
        When: Calling service.find_dish_by_id()
        Then: Raises DishNotFoundException
        """
        # Arrange
        dish_repo = SQLiteDishRepository(test_session)
        restaurant_repo = SQLiteRestaurantRepository(test_session)
        archive_repo = SQLiteArchiveRepository(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        nonexistent_id = generate_ulid()

        # Act & Assert
        with pytest.raises(DishNotFoundException) as exc_info:
            await service.find_dish_by_id(nonexistent_id)

        assert nonexistent_id in str(exc_info.value)
