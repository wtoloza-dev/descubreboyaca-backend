"""Integration tests for RestaurantRepository get operations.

This module tests the get_by_id method with focus on:
- Retrieving existing restaurants
- Handling non-existent IDs
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.repositories import SQLiteRestaurantRepository


class TestRestaurantRepositoryGet:
    """Integration tests for RestaurantRepository get operations."""

    @pytest.mark.asyncio
    async def test_get_by_id_existing(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test getting an existing restaurant by ID.

        Given: A restaurant exists in the database
        When: Calling repository.get_by_id() with valid ID
        Then: Returns the restaurant entity
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        created = await create_test_restaurant(
            name="Test Restaurant",
            city="Tunja",
            description="Integration test",
        )

        # Act
        result = await repository.get_by_id(created.id)

        # Assert
        assert result is not None
        assert result.id == created.id
        assert result.name == "Test Restaurant"
        assert result.city == "Tunja"
        assert result.description == "Integration test"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, test_session: AsyncSession):
        """Test getting non-existent restaurant returns None.

        Given: A restaurant ID that doesn't exist
        When: Calling repository.get_by_id()
        Then: Returns None
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act
        result = await repository.get_by_id(nonexistent_id)

        # Assert
        assert result is None
