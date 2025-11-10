"""E2E tests for admin delete dish endpoint.

This module tests the DELETE /api/v1/restaurants/admin/dishes/{dish_id}
endpoint which allows admins to delete any dish with automatic archiving.
"""

from http import HTTPStatus

import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.infrastructure.persistence.models import ArchiveModel
from app.domains.restaurants.infrastructure.persistence.models import DishModel


class TestAdminDeleteDish:
    """Test suite for DELETE /api/v1/restaurants/admin/dishes/{dish_id}."""

    @pytest.mark.asyncio
    async def test_delete_dish_success(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test successful deletion of a dish by admin with archiving.

        Given: A dish exists
        When: Admin deletes the dish
        Then: Dish is deleted and archived
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Dish to Delete",
            price=10.0,
            category="appetizer",
        )
        dish_id = dish.id

        # Act
        response = admin_client.delete(f"/api/v1/restaurants/admin/dishes/{dish_id}")

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Verify dish is deleted from main table
        result = await test_session.exec(
            select(DishModel).where(DishModel.id == dish_id)
        )
        deleted_dish = result.first()
        assert deleted_dish is None

        # Verify dish is archived
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == dish_id)
        )
        archive = result.first()
        assert archive is not None
        assert archive.original_table == "dishes"
        assert archive.original_id == dish_id
        assert archive.data["name"] == "Dish to Delete"

    @pytest.mark.asyncio
    async def test_delete_dish_from_any_restaurant(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test admin can delete dishes from any restaurant without ownership check.

        Given: Multiple restaurants with dishes exist
        When: Admin deletes dishes from different restaurants
        Then: All dishes are deleted successfully
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="Restaurant 1")
        restaurant2 = await create_test_restaurant(name="Restaurant 2")
        dish1 = await create_test_dish(
            restaurant_id=restaurant1.id,
            name="Dish 1",
        )
        dish2 = await create_test_dish(
            restaurant_id=restaurant2.id,
            name="Dish 2",
        )

        # Act
        response1 = admin_client.delete(f"/api/v1/restaurants/admin/dishes/{dish1.id}")
        response2 = admin_client.delete(f"/api/v1/restaurants/admin/dishes/{dish2.id}")

        # Assert
        assert response1.status_code == HTTPStatus.NO_CONTENT
        assert response2.status_code == HTTPStatus.NO_CONTENT

        # Verify both dishes are deleted
        result = await test_session.exec(
            select(DishModel).where(DishModel.id.in_([dish1.id, dish2.id]))
        )
        assert result.first() is None

    def test_delete_nonexistent_dish(self, admin_client):
        """Test deleting non-existent dish returns 404.

        Given: A dish ID that doesn't exist
        When: Admin tries to delete it
        Then: Returns 404 Not Found
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act
        response = admin_client.delete(
            f"/api/v1/restaurants/admin/dishes/{nonexistent_id}"
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_dish_invalid_id_format(self, admin_client):
        """Test deleting with invalid ULID format returns 422.

        Given: An invalid ULID format
        When: Admin tries to delete it
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        invalid_id = "invalid-id-format"

        # Act
        response = admin_client.delete(f"/api/v1/restaurants/admin/dishes/{invalid_id}")

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_delete_dish_requires_admin_role(self, test_client):
        """Test that delete endpoint requires admin authentication.

        Given: No admin authentication provided
        When: Trying to delete a dish
        Then: Returns 403 or 401

        Note: This test uses regular test_client (no auth override)
        """
        # Act
        response = test_client.delete(
            "/api/v1/restaurants/admin/dishes/01HQZX123456789ABC"
        )

        # Assert
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    @pytest.mark.asyncio
    async def test_delete_archives_complete_dish_data(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test that archive contains complete dish data.

        Given: A dish with complete data exists
        When: Admin deletes the dish
        Then: Archive contains all dish fields
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Complete Dish",
            description="Full description",
            price=25.50,
            category="main_course",
            is_available=True,
            is_featured=True,
        )
        dish_id = dish.id

        # Act
        response = admin_client.delete(f"/api/v1/restaurants/admin/dishes/{dish_id}")

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Verify complete data in archive
        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == dish_id)
        )
        archive = result.first()
        assert archive is not None
        assert archive.data["name"] == "Complete Dish"
        assert archive.data["description"] == "Full description"
        assert archive.data["price"] == "25.50"
        assert archive.data["category"] == "main_course"

    @pytest.mark.asyncio
    async def test_delete_atomicity_documented(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test documenting Unit of Work atomicity guarantees.

        Given: A dish exists
        When: Delete operation succeeds
        Then: Both archive and delete happen atomically

        Note: This test documents the expected behavior. The actual atomicity
        is guaranteed by the AsyncUnitOfWork pattern implemented in the service.

        Unit of Work guarantees:
        - If archive fails → dish NOT deleted (rollback)
        - If delete fails → archive NOT persisted (rollback)
        - If both succeed → both persisted (commit)

        To test actual failure scenarios would require mocking at service/repo level,
        which is better suited for integration tests.
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Test UoW Dish",
        )
        dish_id = dish.id

        # Act
        response = admin_client.delete(f"/api/v1/restaurants/admin/dishes/{dish_id}")

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Verify atomicity: both operations succeeded together
        result = await test_session.exec(
            select(DishModel).where(DishModel.id == dish_id)
        )
        assert result.first() is None  # Dish deleted

        result = await test_session.exec(
            select(ArchiveModel).where(ArchiveModel.original_id == dish_id)
        )
        assert result.first() is not None  # Archive created
