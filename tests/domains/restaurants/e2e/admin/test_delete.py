"""E2E tests for admin delete restaurant endpoint.

This module tests the DELETE /api/v1/admin/restaurants/{restaurant_id} endpoint
which allows admins to delete restaurants with automatic archiving.
"""

import json
from http import HTTPStatus

import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.models import RestaurantModel
from app.shared.models import ArchiveModel


class TestDeleteRestaurant:
    """Test suite for DELETE /api/v1/admin/restaurants/{restaurant_id}."""

    @pytest.mark.asyncio
    async def test_delete_restaurant_success(
        self, admin_client, test_session: AsyncSession, create_test_restaurant
    ):
        """Test successful deletion of a restaurant with archiving.

        Given: A restaurant exists in the database
        When: Admin deletes the restaurant
        Then: Restaurant is deleted and archived
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Restaurant to Delete")
        restaurant_id = restaurant.id

        # Act
        response = admin_client.request(
            "DELETE",
            f"/api/v1/restaurants/admin/{restaurant_id}",
            content=json.dumps({"note": "Closed permanently"}),
            headers={"Content-Type": "application/json"},
        )

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Verify restaurant is deleted from main table
        result = await test_session.exec(
            select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        )
        deleted_restaurant = result.first()
        assert deleted_restaurant is None

        # Verify restaurant is archived
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        archive = result.first()
        assert archive is not None
        assert archive.original_table == "restaurants"
        assert archive.original_id == restaurant_id
        assert archive.data["name"] == "Restaurant to Delete"
        assert archive.note == "Closed permanently"

    @pytest.mark.asyncio
    async def test_delete_restaurant_without_note(
        self, admin_client, test_session: AsyncSession, create_test_restaurant
    ):
        """Test deletion without a note is allowed.

        Given: A restaurant exists
        When: Admin deletes without providing a note
        Then: Restaurant is deleted and archived without note
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Restaurant No Note")
        restaurant_id = restaurant.id

        # Act
        response = admin_client.delete(f"/api/v1/restaurants/admin/{restaurant_id}")

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Verify archived without note
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        archive = result.first()
        assert archive is not None
        assert archive.note is None

    def test_delete_nonexistent_restaurant(self, admin_client):
        """Test deleting a non-existent restaurant returns 404.

        Given: A restaurant ID that doesn't exist
        When: Admin tries to delete it
        Then: Returns 404 Not Found
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act
        response = admin_client.request(
            "DELETE",
            f"/api/v1/restaurants/admin/{nonexistent_id}",
            content=json.dumps({"note": "Should fail"}),
            headers={"Content-Type": "application/json"},
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_with_invalid_id_format(self, admin_client):
        """Test deleting with invalid ULID format returns 422.

        Given: An invalid ULID format
        When: Admin tries to delete it
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        invalid_id = "invalid-id-format"

        # Act
        response = admin_client.delete(f"/api/v1/restaurants/admin/{invalid_id}")

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_delete_archives_complete_data(
        self, admin_client, test_session: AsyncSession, create_test_restaurant
    ):
        """Test that archive contains complete restaurant data.

        Given: A restaurant with complete data exists
        When: Admin deletes the restaurant
        Then: Archive contains all restaurant fields
        """
        # Arrange
        restaurant = await create_test_restaurant(
            name="Complete Restaurant",
            description="Full description",
            email="complete@restaurant.com",
            phone="+57 300 123 4567",
            price_level=3,
        )
        restaurant_id = restaurant.id

        # Act
        response = admin_client.request(
            "DELETE",
            f"/api/v1/restaurants/admin/{restaurant_id}",
            content=json.dumps({"note": "Archiving complete data"}),
            headers={"Content-Type": "application/json"},
        )

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Verify complete data in archive
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        archive = result.first()
        assert archive is not None
        assert archive.data["name"] == "Complete Restaurant"
        assert archive.data["description"] == "Full description"
        assert archive.data["email"] == "complete@restaurant.com"
        assert archive.data["phone"] == "+57 300 123 4567"
        assert archive.data["price_level"] == 3

    @pytest.mark.asyncio
    async def test_delete_atomicity_documented(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
    ):
        """Test documenting Unit of Work atomicity guarantees.

        Given: A restaurant exists
        When: Delete operation succeeds
        Then: Both archive and delete happen atomically

        Note: This test documents the expected behavior. The actual atomicity
        is guaranteed by the AsyncUnitOfWork pattern implemented in the service.

        Unit of Work guarantees:
        - If archive fails → restaurant NOT deleted (rollback)
        - If delete fails → archive NOT persisted (rollback)
        - If both succeed → both persisted (commit)

        To test actual failure scenarios would require mocking at service/repo level,
        which is better suited for integration tests.
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test UoW")
        restaurant_id = restaurant.id

        # Act
        response = admin_client.delete(f"/api/v1/restaurants/admin/{restaurant_id}")

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Verify atomicity: both operations succeeded together
        result = await test_session.exec(
            select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        )
        assert result.first() is None  # Restaurant deleted

        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == restaurant_id)
        )
        assert result.first() is not None  # Archive created

    def test_delete_requires_admin_role(self, test_client, create_test_restaurant):
        """Test that delete endpoint requires admin authentication.

        Given: No authentication provided
        When: Trying to delete a restaurant
        Then: Returns 403 or 401 (depending on implementation)

        Note: This test uses regular test_client (no auth override)
        """
        # Arrange - using regular test_client without auth
        # (admin_client has auth bypassed)

        # Act
        response = test_client.delete("/api/v1/restaurants/admin/01HQZX123456789ABC")

        # Assert
        # Should fail due to missing/invalid authentication
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]
