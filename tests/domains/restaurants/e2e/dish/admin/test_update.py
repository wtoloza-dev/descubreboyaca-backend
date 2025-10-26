"""E2E tests for admin update dish endpoint.

This module tests the PATCH /api/v1/restaurants/admin/dishes/{dish_id}
endpoint which allows admins to update any dish.
"""

from http import HTTPStatus

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession


class TestAdminUpdateDish:
    """Test suite for PATCH /api/v1/restaurants/admin/dishes/{dish_id}."""

    @pytest.mark.asyncio
    async def test_update_dish_success(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test successful update of a dish by admin.

        Given: A dish exists
        When: Admin updates the dish
        Then: Dish is updated successfully
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Original Name",
            price=10.0,
            category="appetizer",
        )

        update_data = {
            "name": "Updated Name",
            "price": 15.0,
        }

        # Act
        response = admin_client.patch(
            f"/api/v1/restaurants/admin/dishes/{dish.id}",
            json=update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["price"] == "15.00"
        assert data["category"] == "appetizer"  # Unchanged

        # Verify in database
        await test_session.refresh(dish)
        assert dish.name == "Updated Name"
        assert dish.price == 15.0

    @pytest.mark.asyncio
    async def test_update_dish_partial_fields(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test updating only specific fields (PATCH behavior).

        Given: A dish with complete data exists
        When: Admin updates only one field
        Then: Only that field is updated, others remain unchanged
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Original Dish",
            description="Original description",
            price=20.0,
            category="main_course",
            is_available=True,
        )

        update_data = {"price": 25.0}

        # Act
        response = admin_client.patch(
            f"/api/v1/restaurants/admin/dishes/{dish.id}",
            json=update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["name"] == "Original Dish"  # Unchanged
        assert data["description"] == "Original description"  # Unchanged
        assert data["price"] == "25.00"  # Updated
        assert data["category"] == "main_course"  # Unchanged

    @pytest.mark.asyncio
    async def test_update_dish_from_any_restaurant(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test admin can update dishes from any restaurant without ownership check.

        Given: Multiple restaurants with dishes exist
        When: Admin updates dishes from different restaurants
        Then: All dishes are updated successfully
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="Restaurant 1")
        restaurant2 = await create_test_restaurant(name="Restaurant 2")
        dish1 = await create_test_dish(
            restaurant_id=restaurant1.id,
            name="Dish 1",
            price=10.0,
        )
        dish2 = await create_test_dish(
            restaurant_id=restaurant2.id,
            name="Dish 2",
            price=20.0,
        )

        # Act
        response1 = admin_client.patch(
            f"/api/v1/restaurants/admin/dishes/{dish1.id}",
            json={"price": 12.0},
        )
        response2 = admin_client.patch(
            f"/api/v1/restaurants/admin/dishes/{dish2.id}",
            json={"price": 22.0},
        )

        # Assert
        assert response1.status_code == HTTPStatus.OK
        assert response2.status_code == HTTPStatus.OK
        assert response1.json()["price"] == "12.00"
        assert response2.json()["price"] == "22.00"

    def test_update_nonexistent_dish(self, admin_client):
        """Test updating non-existent dish returns 404.

        Given: A dish ID that doesn't exist
        When: Admin tries to update it
        Then: Returns 404 Not Found
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"
        update_data = {"price": 15.0}

        # Act
        response = admin_client.patch(
            f"/api/v1/restaurants/admin/dishes/{nonexistent_id}",
            json=update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_dish_invalid_id_format(self, admin_client):
        """Test updating with invalid ULID format returns 422.

        Given: An invalid ULID format
        When: Admin tries to update it
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        invalid_id = "invalid-id-format"
        update_data = {"price": 15.0}

        # Act
        response = admin_client.patch(
            f"/api/v1/restaurants/admin/dishes/{invalid_id}",
            json=update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_update_dish_requires_admin_role(self, test_client):
        """Test that update endpoint requires admin authentication.

        Given: No admin authentication provided
        When: Trying to update a dish
        Then: Returns 403 or 401

        Note: This test uses regular test_client (no auth override)
        """
        # Arrange
        update_data = {"price": 15.0}

        # Act
        response = test_client.patch(
            "/api/v1/restaurants/admin/dishes/01HQZX123456789ABC",
            json=update_data,
        )

        # Assert
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    @pytest.mark.asyncio
    async def test_update_dish_availability_toggle(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test admin can toggle dish availability.

        Given: A dish that is available
        When: Admin sets it to unavailable
        Then: Dish availability is updated
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Available Dish",
            is_available=True,
        )

        # Act
        response = admin_client.patch(
            f"/api/v1/restaurants/admin/dishes/{dish.id}",
            json={"is_available": False},
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.json()["is_available"] is False

    @pytest.mark.asyncio
    async def test_update_dish_featured_status(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test admin can update featured status.

        Given: A regular dish exists
        When: Admin marks it as featured
        Then: Dish is marked as featured
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Regular Dish",
            is_featured=False,
        )

        # Act
        response = admin_client.patch(
            f"/api/v1/restaurants/admin/dishes/{dish.id}",
            json={"is_featured": True},
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.json()["is_featured"] is True
