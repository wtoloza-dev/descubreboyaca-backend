"""Integration tests for RestaurantService get operations.

This module tests the get_restaurant_by_id method with focus on:
- Retrieving existing restaurants
- Error handling for non-existent restaurants
- Service-repository integration
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.domain.exceptions import RestaurantNotFoundException
from app.domains.restaurants.repositories import RestaurantRepositorySQLite
from app.domains.restaurants.services import RestaurantService
from app.shared.repositories.archive import AsyncArchiveRepositorySQLite


class TestRestaurantServiceGet:
    """Integration tests for RestaurantService.get_restaurant_by_id()."""

    @pytest.mark.asyncio
    async def test_get_restaurant_by_id_existing(
        self, test_session: AsyncSession, create_test_restaurant
    ):
        """Test getting an existing restaurant through service layer.

        Given: A restaurant exists in the database
        When: Calling service.get_restaurant_by_id() with valid ID
        Then: Returns the restaurant entity with correct data
        """
        # Arrange
        restaurant_repo = RestaurantRepositorySQLite(test_session)
        archive_repo = AsyncArchiveRepositorySQLite(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        created = await create_test_restaurant(
            name="Integration Test Restaurant",
            city="Tunja",
            description="Testing service layer",
        )

        # Act
        result = await service.get_restaurant_by_id(created.id)

        # Assert
        assert result.id == created.id
        assert result.name == "Integration Test Restaurant"
        assert result.city == "Tunja"
        assert result.description == "Testing service layer"

    @pytest.mark.asyncio
    async def test_get_restaurant_by_id_not_found(self, test_session: AsyncSession):
        """Test getting non-existent restaurant raises exception.

        Given: A restaurant ID that doesn't exist in database
        When: Calling service.get_restaurant_by_id()
        Then: Raises RestaurantNotFoundException
        """
        # Arrange
        restaurant_repo = RestaurantRepositorySQLite(test_session)
        archive_repo = AsyncArchiveRepositorySQLite(test_session)
        service = RestaurantService(restaurant_repo, archive_repo)

        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act & Assert
        with pytest.raises(RestaurantNotFoundException) as exc_info:
            await service.get_restaurant_by_id(nonexistent_id)

        assert nonexistent_id in str(exc_info.value)
