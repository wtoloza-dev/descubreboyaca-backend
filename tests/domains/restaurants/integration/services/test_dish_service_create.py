"""Integration tests for DishService create operations.

This module tests the create_dish method of DishService.
"""

from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain import DishData
from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.repositories.dish.sqlite import DishRepositorySQLite
from app.domains.restaurants.repositories.restaurant.sqlite import (
    RestaurantRepositorySQLite,
)
from app.domains.restaurants.services.dish import DishService
from app.shared.domain.factories import generate_ulid
from app.shared.repositories.archive.sqlite import ArchiveRepositorySQLite


class TestDishServiceCreate:
    """Integration tests for DishService create operations."""

    @pytest.mark.asyncio
    async def test_create_dish_success(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        sample_dish_data: DishData,
    ):
        """Test creating a dish for existing restaurant succeeds.

        Given: A restaurant exists and valid dish data
        When: Calling service.create_dish()
        Then: Dish is created with ID and metadata
        """
        # Arrange
        dish_repo = DishRepositorySQLite(test_session)
        restaurant_repo = RestaurantRepositorySQLite(test_session)
        archive_repo = ArchiveRepositorySQLite(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        restaurant = await create_test_restaurant(name="Test Restaurant")

        # Act
        result = await service.create_dish(
            sample_dish_data, restaurant_id=restaurant.id
        )

        # Assert
        assert result.id is not None
        assert result.restaurant_id == restaurant.id
        assert result.name == sample_dish_data.name
        assert result.category == sample_dish_data.category
        assert result.price == sample_dish_data.price
        assert result.created_at is not None

    @pytest.mark.asyncio
    async def test_create_dish_nonexistent_restaurant(
        self,
        test_session: AsyncSession,
        sample_dish_data: DishData,
    ):
        """Test creating dish for non-existent restaurant raises exception.

        Given: Restaurant ID that doesn't exist
        When: Calling service.create_dish()
        Then: Raises RestaurantNotFoundException
        """
        # Arrange
        dish_repo = DishRepositorySQLite(test_session)
        restaurant_repo = RestaurantRepositorySQLite(test_session)
        archive_repo = ArchiveRepositorySQLite(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        nonexistent_id = generate_ulid()

        # Act & Assert
        with pytest.raises(RestaurantNotFoundException) as exc_info:
            await service.create_dish(sample_dish_data, restaurant_id=nonexistent_id)

        assert nonexistent_id in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_dish_with_minimal_data(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
    ):
        """Test creating dish with only required fields.

        Given: A restaurant exists and minimal dish data
        When: Calling service.create_dish()
        Then: Dish is created with defaults for optional fields
        """
        # Arrange
        dish_repo = DishRepositorySQLite(test_session)
        restaurant_repo = RestaurantRepositorySQLite(test_session)
        archive_repo = ArchiveRepositorySQLite(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        restaurant = await create_test_restaurant(name="Test Restaurant")

        minimal_data = DishData(
            name="Simple Dish",
            category="dessert",
            price=Decimal("8000.00"),
        )

        # Act
        result = await service.create_dish(minimal_data, restaurant_id=restaurant.id)

        # Assert
        assert result.id is not None
        assert result.name == "Simple Dish"
        assert result.description is None
        assert result.is_available is True  # Default value
        assert result.is_featured is False  # Default value
        assert result.display_order == 0  # Default value

    @pytest.mark.asyncio
    async def test_create_dish_with_created_by(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        sample_dish_data: DishData,
    ):
        """Test creating dish tracks the creator.

        Given: A restaurant exists and a user ID
        When: Creating dish with created_by parameter
        Then: Audit trail includes created_by user ID
        """
        # Arrange
        dish_repo = DishRepositorySQLite(test_session)
        restaurant_repo = RestaurantRepositorySQLite(test_session)
        archive_repo = ArchiveRepositorySQLite(test_session)
        service = DishService(dish_repo, restaurant_repo, archive_repo)

        restaurant = await create_test_restaurant(name="Test Restaurant")
        creator_id = generate_ulid()

        # Act
        result = await service.create_dish(
            sample_dish_data, restaurant_id=restaurant.id, created_by=creator_id
        )

        # Assert
        assert result.created_by == creator_id
        assert result.updated_by == creator_id
