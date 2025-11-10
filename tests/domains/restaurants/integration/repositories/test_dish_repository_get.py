"""Integration tests for DishRepository get operations.

This module tests the get_by_id method of DishRepositorySQLite.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.infrastructure.persistence.repositories.dish.sqlite import (
    SQLiteDishRepository,
)
from app.shared.domain.factories import generate_ulid


class TestDishRepositoryGet:
    """Integration tests for DishRepository get operations."""

    @pytest.mark.asyncio
    async def test_get_by_id_existing(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test getting an existing dish by ID.

        Given: A dish exists in database
        When: Calling repository.get_by_id()
        Then: Returns dish entity
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        created = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Test Dish",
        )

        # Act
        result = await repository.get_by_id(created.id)

        # Assert
        assert result is not None
        assert result.id == created.id
        assert result.name == "Test Dish"
        assert result.restaurant_id == restaurant.id

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, test_session: AsyncSession):
        """Test getting non-existent dish returns None.

        Given: Dish ID that doesn't exist
        When: Calling repository.get_by_id()
        Then: Returns None
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        nonexistent_id = generate_ulid()

        # Act
        result = await repository.get_by_id(nonexistent_id)

        # Assert
        assert result is None
