"""E2E tests for owner update dish endpoint.

This module tests the PATCH /api/v1/restaurants/owner/dishes/{dish_id}
endpoint which allows restaurant owners to update their dishes.
"""

from http import HTTPStatus

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession


class TestOwnerUpdateDish:
    """Test suite for PATCH /api/v1/restaurants/owner/dishes/{dish_id}."""

    @pytest.mark.asyncio
    async def test_update_dish_success(
        self,
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
        create_test_dish,
    ):
        """Test successful update of a dish by owner.

        Given: An owner has a restaurant with a dish
        When: Owner updates the dish
        Then: Dish is updated successfully
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
            name="Original Name",
            price=10.0,
            category="appetizer",
        )

        update_data = {
            "name": "Updated Name",
            "price": 15.0,
        }

        # Act
        response = owner_client.patch(
            f"/api/v1/restaurants/owner/dishes/{dish.id}",
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
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
        create_test_dish,
    ):
        """Test updating only specific fields (PATCH behavior).

        Given: A dish with complete data exists
        When: Owner updates only one field
        Then: Only that field is updated, others remain unchanged
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
            name="Original Dish",
            description="Original description",
            price=20.0,
            category="main_course",
            is_available=True,
        )

        update_data = {"price": 25.0}

        # Act
        response = owner_client.patch(
            f"/api/v1/restaurants/owner/dishes/{dish.id}",
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
    async def test_update_dish_not_owner(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test owner cannot update dish from restaurant they don't own.

        Given: A dish exists in a restaurant the owner doesn't own
        When: Owner tries to update that dish
        Then: Returns 403 Forbidden
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Someone Else's Restaurant")
        # Note: No ownership created for mock_owner_user
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Original Dish",
            price=10.0,
        )

        update_data = {"price": 15.0}

        # Act
        response = owner_client.patch(
            f"/api/v1/restaurants/owner/dishes/{dish.id}",
            json=update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_update_nonexistent_dish(self, owner_client):
        """Test updating non-existent dish returns 404.

        Given: A dish ID that doesn't exist
        When: Owner tries to update it
        Then: Returns 404 Not Found
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"
        update_data = {"price": 15.0}

        # Act
        response = owner_client.patch(
            f"/api/v1/restaurants/owner/dishes/{nonexistent_id}",
            json=update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_update_dish_invalid_id_format(self, owner_client):
        """Test updating with invalid ULID format returns 422.

        Given: An invalid ULID format
        When: Owner tries to update it
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        invalid_id = "invalid-id-format"
        update_data = {"price": 15.0}

        # Act
        response = owner_client.patch(
            f"/api/v1/restaurants/owner/dishes/{invalid_id}",
            json=update_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_update_dish_requires_owner_role(self, test_client):
        """Test that update endpoint requires owner authentication.

        Given: No owner authentication provided
        When: Trying to update a dish
        Then: Returns 403 or 401

        Note: This test uses regular test_client (no auth override)
        """
        # Arrange
        update_data = {"price": 15.0}

        # Act
        response = test_client.patch(
            "/api/v1/restaurants/owner/dishes/01HQZX123456789ABC",
            json=update_data,
        )

        # Assert
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    @pytest.mark.asyncio
    async def test_update_dish_availability_toggle(
        self,
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
        create_test_dish,
    ):
        """Test owner can toggle dish availability.

        Given: A dish that is available
        When: Owner sets it to unavailable
        Then: Dish availability is updated
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
            name="Available Dish",
            is_available=True,
        )

        # Act
        response = owner_client.patch(
            f"/api/v1/restaurants/owner/dishes/{dish.id}",
            json={"is_available": False},
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.json()["is_available"] is False

    @pytest.mark.asyncio
    async def test_update_dish_as_manager(
        self,
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
        create_test_dish,
    ):
        """Test manager can update dishes from managed restaurant.

        Given: A user is a manager of a restaurant
        When: Manager updates a dish
        Then: Dish is updated successfully
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
            name="Dish to Update",
            price=10.0,
        )

        # Act
        response = owner_client.patch(
            f"/api/v1/restaurants/owner/dishes/{dish.id}",
            json={"price": 12.0},
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        assert response.json()["price"] == "12.00"
