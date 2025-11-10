"""Integration tests for RestaurantRepository create operations.

This module tests the create method with focus on:
- Creating and persisting restaurants
- Auto-generating IDs
- Data integrity
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain import RestaurantData
from app.domains.restaurants.infrastructure.persistence.repositories import (
    SQLiteRestaurantRepository,
)


class TestRestaurantRepositoryCreate:
    """Integration tests for RestaurantRepository create operations."""

    @pytest.mark.asyncio
    async def test_create_restaurant_saves_to_database(
        self, test_session: AsyncSession
    ):
        """Test creating a restaurant persists to database.

        Given: Valid restaurant data
        When: Calling repository.create()
        Then: Restaurant is saved and can be retrieved
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        restaurant_data = RestaurantData(
            name="New Restaurant",
            address="Calle 1 #2-3",
            city="Tunja",
            state="Boyacá",
            country="Colombia",
            phone="+57 300 123 4567",
            cuisine_types=["Colombiana"],
            features=["wifi"],
        )

        # Act
        created = await repository.create(restaurant_data, commit=True)

        # Assert
        assert created.name == "New Restaurant"
        assert created.city == "Tunja"
        assert created.id is not None  # ID should be auto-generated

        # Verify it's actually in DB
        retrieved = await repository.get_by_id(created.id)
        assert retrieved is not None
        assert retrieved.name == "New Restaurant"
