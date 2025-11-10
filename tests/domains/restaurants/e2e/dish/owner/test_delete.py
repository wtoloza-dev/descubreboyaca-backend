"""E2E tests for owner delete dish endpoint.

This module tests the DELETE /api/v1/restaurants/owner/dishes/{dish_id}
endpoint which allows restaurant owners to delete their dishes with automatic archiving.
"""

from http import HTTPStatus

import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.audit.infrastructure.persistence.models import ArchiveModel
from app.domains.restaurants.infrastructure.persistence.models import DishModel


class TestOwnerDeleteDish:
    """Test suite for DELETE /api/v1/restaurants/owner/dishes/{dish_id}."""

    @pytest.mark.asyncio
    async def test_delete_dish_success(
        self,
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
        create_test_dish,
    ):
        """Test successful deletion of a dish by owner with archiving.

        Given: An owner has a restaurant with a dish
        When: Owner deletes the dish
        Then: Dish is deleted and archived
        """
        # Arrange
        restaurant = await create_test_restaurant(name="My Restaurant")
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="owner",
            is_primary=True,
        )
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Dish to Delete",
            price=10.0,
            category="appetizer",
        )
        dish_id = dish.id

        # Act
        response = owner_client.delete(f"/api/v1/restaurants/owner/dishes/{dish_id}")

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
    async def test_delete_dish_not_owner(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test owner cannot delete dish from restaurant they don't own.

        Given: A dish exists in a restaurant the owner doesn't own
        When: Owner tries to delete that dish
        Then: Returns 403 Forbidden
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Someone Else's Restaurant")
        # Note: No ownership created for mock_owner_user
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Protected Dish",
        )

        # Act
        response = owner_client.delete(f"/api/v1/restaurants/owner/dishes/{dish.id}")

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_delete_nonexistent_dish(self, owner_client):
        """Test deleting non-existent dish returns 404.

        Given: A dish ID that doesn't exist
        When: Owner tries to delete it
        Then: Returns 404 Not Found
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"

        # Act
        response = owner_client.delete(
            f"/api/v1/restaurants/owner/dishes/{nonexistent_id}"
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_dish_invalid_id_format(self, owner_client):
        """Test deleting with invalid ULID format returns 422.

        Given: An invalid ULID format
        When: Owner tries to delete it
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        invalid_id = "invalid-id-format"

        # Act
        response = owner_client.delete(f"/api/v1/restaurants/owner/dishes/{invalid_id}")

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_delete_dish_requires_owner_role(self, test_client):
        """Test that delete endpoint requires owner authentication.

        Given: No owner authentication provided
        When: Trying to delete a dish
        Then: Returns 403 or 401

        Note: This test uses regular test_client (no auth override)
        """
        # Act
        response = test_client.delete(
            "/api/v1/restaurants/owner/dishes/01HQZX123456789ABC"
        )

        # Assert
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    @pytest.mark.asyncio
    async def test_delete_archives_complete_dish_data(
        self,
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
        create_test_dish,
    ):
        """Test that archive contains complete dish data.

        Given: A dish with complete data exists
        When: Owner deletes the dish
        Then: Archive contains all dish fields
        """
        # Arrange
        restaurant = await create_test_restaurant(name="My Restaurant")
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="owner",
            is_primary=True,
        )
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
        response = owner_client.delete(f"/api/v1/restaurants/owner/dishes/{dish_id}")

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
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
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
        restaurant = await create_test_restaurant(name="My Restaurant")
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="owner",
            is_primary=True,
        )
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Test UoW Dish",
        )
        dish_id = dish.id

        # Act
        response = owner_client.delete(f"/api/v1/restaurants/owner/dishes/{dish_id}")

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

    @pytest.mark.asyncio
    async def test_delete_dish_as_manager(
        self,
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
        create_test_dish,
    ):
        """Test manager can delete dishes from managed restaurant.

        Given: A user is a manager of a restaurant
        When: Manager deletes a dish
        Then: Dish is deleted successfully
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Managed Restaurant")
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="manager",  # Manager role
            is_primary=False,
        )
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Dish to Delete",
        )
        dish_id = dish.id

        # Act
        response = owner_client.delete(f"/api/v1/restaurants/owner/dishes/{dish_id}")

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Verify dish is deleted
        result = await test_session.exec(
            select(DishModel).where(DishModel.id == dish_id)
        )
        assert result.first() is None
