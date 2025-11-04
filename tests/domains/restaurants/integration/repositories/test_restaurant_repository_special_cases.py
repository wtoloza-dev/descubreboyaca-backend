"""Integration tests for RestaurantRepository special cases.

This module tests edge cases and special scenarios:
- City names with special characters (spaces)
- City names with accents
- Limit parameter enforcement
- Character encoding
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.repositories import SQLiteRestaurantRepository


class TestRestaurantRepositorySpecialCases:
    """Integration tests for special cases and edge conditions."""

    @pytest.mark.asyncio
    async def test_find_with_special_characters_in_city(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test finding restaurants with city names containing special characters.

        Given: Restaurant in "Villa de Leyva" (with spaces)
        When: Calling repository.find() with city filter
        Then: Returns restaurant with exact match
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        await create_test_restaurant(name="Villa Restaurant", city="Villa de Leyva")
        await create_test_restaurant(name="Tunja Restaurant", city="Tunja")

        # Act
        results = await repository.find(
            filters={"city": "Villa de Leyva"}, offset=0, limit=10
        )

        # Assert
        assert len(results) == 1
        assert results[0].city == "Villa de Leyva"
        assert results[0].name == "Villa Restaurant"

    @pytest.mark.asyncio
    async def test_find_with_accents_in_city(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test finding restaurants with city names containing accents.

        Given: Restaurant in "Bogotá" (with accent)
        When: Calling repository.find() with city filter
        Then: Returns restaurant with exact match
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        await create_test_restaurant(name="Bogotá Restaurant", city="Bogotá")
        await create_test_restaurant(name="Other Restaurant", city="Bogota")

        # Act
        results = await repository.find(filters={"city": "Bogotá"}, offset=0, limit=10)

        # Assert
        assert len(results) == 1
        assert results[0].city == "Bogotá"

    @pytest.mark.asyncio
    async def test_find_respects_limit(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test that find respects the limit parameter.

        Given: 10 restaurants in database
        When: Calling repository.find() with limit=3
        Then: Returns exactly 3 restaurants
        """
        # Arrange
        repository = SQLiteRestaurantRepository(test_session)
        for i in range(10):
            await create_test_restaurant(name=f"Restaurant {i:02d}", city="Tunja")

        # Act
        results = await repository.find(filters=None, offset=0, limit=3)

        # Assert
        assert len(results) == 3
