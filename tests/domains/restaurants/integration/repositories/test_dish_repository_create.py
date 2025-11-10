"""Integration tests for DishRepository create operations.

This module tests the create method of DishRepositorySQLite.
"""

from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain import DishData
from app.domains.restaurants.infrastructure.persistence.repositories.dish.sqlite import (
    SQLiteDishRepository,
)
from app.shared.domain.factories import generate_ulid


class TestDishRepositoryCreate:
    """Integration tests for DishRepository create operations."""

    @pytest.mark.asyncio
    async def test_create_dish_with_full_data(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        sample_dish_data: DishData,
    ):
        """Test creating a dish with complete data.

        Given: Valid dish data and existing restaurant
        When: Calling repository.create()
        Then: Dish is persisted with ID and audit fields
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")

        # Act
        result = await repository.create(sample_dish_data, restaurant_id=restaurant.id)

        # Assert
        assert result.id is not None
        assert result.restaurant_id == restaurant.id
        assert result.name == sample_dish_data.name
        assert result.category == sample_dish_data.category
        assert result.price == sample_dish_data.price
        assert result.created_at is not None
        assert result.updated_at is not None

    @pytest.mark.asyncio
    async def test_create_dish_with_minimal_data(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
    ):
        """Test creating dish with only required fields.

        Given: Minimal dish data and existing restaurant
        When: Calling repository.create()
        Then: Dish is persisted with default values for optional fields
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")

        minimal_data = DishData(
            name="Simple Dish",
            category="dessert",
            price=Decimal("8000.00"),
        )

        # Act
        result = await repository.create(minimal_data, restaurant_id=restaurant.id)

        # Assert
        assert result.id is not None
        assert result.name == "Simple Dish"
        assert result.description is None
        assert result.is_available is True
        assert result.is_featured is False
        assert result.display_order == 0
        assert result.dietary_restrictions == []
        assert result.ingredients == []
        assert result.allergens == []
        assert result.flavor_profile == {}

    @pytest.mark.asyncio
    async def test_create_dish_with_created_by(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        sample_dish_data: DishData,
    ):
        """Test creating dish with creator tracking.

        Given: Dish data and a creator user ID
        When: Creating dish with created_by parameter
        Then: Audit trail includes creator ID
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")
        creator_id = generate_ulid()

        # Act
        result = await repository.create(
            sample_dish_data, restaurant_id=restaurant.id, created_by=creator_id
        )

        # Assert
        assert result.created_by == creator_id
        assert result.updated_by == creator_id

    @pytest.mark.asyncio
    async def test_create_dish_generates_unique_ids(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        sample_dish_data: DishData,
    ):
        """Test that each created dish gets a unique ID.

        Given: Same dish data used twice
        When: Creating two dishes
        Then: Each has a different unique ID
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")

        # Act
        result1 = await repository.create(sample_dish_data, restaurant_id=restaurant.id)
        result2 = await repository.create(sample_dish_data, restaurant_id=restaurant.id)

        # Assert
        assert result1.id != result2.id
        assert len(result1.id) == 26  # ULID length
        assert len(result2.id) == 26

    @pytest.mark.asyncio
    async def test_create_dish_can_retrieve_after_creation(
        self,
        test_session: AsyncSession,
        create_test_restaurant,
        sample_dish_data: DishData,
    ):
        """Test that created dish can be retrieved from database.

        Given: A dish is created
        When: Retrieving by its ID
        Then: Returns the same dish with all data intact
        """
        # Arrange
        repository = SQLiteDishRepository(test_session)
        restaurant = await create_test_restaurant(name="Test Restaurant")

        # Act
        created = await repository.create(sample_dish_data, restaurant_id=restaurant.id)
        retrieved = await repository.get_by_id(created.id)

        # Assert
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == created.name
        assert retrieved.category == created.category
        assert retrieved.price == created.price
