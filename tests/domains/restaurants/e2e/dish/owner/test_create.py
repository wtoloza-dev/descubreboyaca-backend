"""E2E tests for owner create dish endpoint.

This module tests the POST /api/v1/restaurants/owner/restaurants/{restaurant_id}/dishes
endpoint which allows restaurant owners to create dishes for their restaurants.
"""

from http import HTTPStatus

import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.models import DishModel


class TestOwnerCreateDish:
    """Test suite for POST /api/v1/restaurants/owner/restaurants/{restaurant_id}/dishes."""

    @pytest.mark.asyncio
    async def test_create_dish_success(
        self,
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test successful creation of a dish by restaurant owner.

        Given: An owner has a restaurant
        When: Owner creates a dish for their restaurant
        Then: Dish is created successfully
        """
        # Arrange
        restaurant = await create_test_restaurant(name="My Restaurant")
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="owner",
            is_primary=True,
        )

        dish_data = {
            "name": "Owner Created Dish",
            "description": "Created by owner",
            "price": 15.99,
            "category": "main_course",
            "is_available": True,
            "is_featured": False,
        }

        # Act
        response = owner_client.post(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["name"] == "Owner Created Dish"
        assert data["description"] == "Created by owner"
        assert data["price"] == "15.99"
        assert data["category"] == "main_course"
        assert data["restaurant_id"] == restaurant.id

        # Verify in database
        result = await test_session.exec(
            select(DishModel).where(DishModel.id == data["id"])
        )
        created_dish = result.first()
        assert created_dish is not None
        assert created_dish.name == "Owner Created Dish"

    @pytest.mark.asyncio
    async def test_create_dish_not_owner(
        self,
        owner_client,
        mock_owner_user,
        create_test_restaurant,
    ):
        """Test owner cannot create dish for restaurant they don't own.

        Given: A restaurant exists that the owner doesn't own
        When: Owner tries to create a dish for that restaurant
        Then: Returns 403 Forbidden
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Someone Else's Restaurant")
        # Note: No ownership created for mock_owner_user

        dish_data = {
            "name": "Unauthorized Dish",
            "price": 10.0,
            "category": "appetizer",
        }

        # Act
        response = owner_client.post(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_create_dish_nonexistent_restaurant(self, owner_client):
        """Test creating dish for non-existent restaurant returns 403.

        Given: A restaurant ID that doesn't exist (and owner doesn't have access)
        When: Owner tries to create a dish for it
        Then: Returns 403 Forbidden (ownership check happens first)

        Note: The ownership verification happens before checking if the restaurant
        exists, so we get 403 instead of 404. This is a security best practice
        to avoid leaking information about resource existence.
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"
        dish_data = {
            "name": "Test Dish",
            "price": 10.0,
            "category": "appetizer",
        }

        # Act
        response = owner_client.post(
            f"/api/v1/restaurants/owner/restaurants/{nonexistent_id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_create_dish_invalid_restaurant_id(self, owner_client):
        """Test creating dish with invalid restaurant ID returns 422.

        Given: An invalid ULID format
        When: Owner tries to create a dish
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        invalid_id = "invalid-id-format"
        dish_data = {
            "name": "Test Dish",
            "price": 10.0,
            "category": "appetizer",
        }

        # Act
        response = owner_client.post(
            f"/api/v1/restaurants/owner/restaurants/{invalid_id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_dish_missing_required_fields(self, owner_client):
        """Test creating dish without required fields returns 422.

        Given: A valid restaurant ID
        When: Owner tries to create dish without required fields
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        dish_data = {
            "description": "Missing name and price",
        }

        # Act
        response = owner_client.post(
            "/api/v1/restaurants/owner/restaurants/01HQZX123456789ABCDEFGHIJK/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_dish_requires_owner_role(self, test_client):
        """Test that create endpoint requires owner authentication.

        Given: No owner authentication provided
        When: Trying to create a dish
        Then: Returns 403 or 401

        Note: This test uses regular test_client (no auth override)
        """
        # Arrange
        dish_data = {
            "name": "Test Dish",
            "price": 10.0,
            "category": "appetizer",
        }

        # Act
        response = test_client.post(
            "/api/v1/restaurants/owner/restaurants/01HQZX123456789ABC/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    @pytest.mark.asyncio
    async def test_create_dish_as_manager(
        self,
        owner_client,
        mock_owner_user,
        test_session: AsyncSession,
        create_test_restaurant,
        create_test_ownership,
    ):
        """Test manager can create dishes for managed restaurant.

        Given: A user is a manager of a restaurant
        When: Manager creates a dish
        Then: Dish is created successfully
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Managed Restaurant")
        await create_test_ownership(
            owner_id=mock_owner_user.id,
            restaurant_id=restaurant.id,
            role="manager",  # Manager role
            is_primary=False,
        )

        dish_data = {
            "name": "Manager Created Dish",
            "price": 12.0,
            "category": "dessert",
        }

        # Act
        response = owner_client.post(
            f"/api/v1/restaurants/owner/restaurants/{restaurant.id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["name"] == "Manager Created Dish"
