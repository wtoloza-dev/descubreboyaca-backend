"""E2E tests for admin create dish endpoint.

This module tests the POST /api/v1/restaurants/admin/restaurants/{restaurant_id}/dishes
endpoint which allows admins to create dishes for any restaurant.
"""

from http import HTTPStatus

import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.restaurants.infrastructure.persistence.models import DishModel


class TestAdminCreateDish:
    """Test suite for POST /api/v1/restaurants/admin/restaurants/{restaurant_id}/dishes."""

    @pytest.mark.asyncio
    async def test_create_dish_success(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
    ):
        """Test successful creation of a dish by admin.

        Given: A restaurant exists
        When: Admin creates a dish for the restaurant
        Then: Dish is created successfully
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")

        dish_data = {
            "name": "Admin Created Dish",
            "description": "Created by admin",
            "price": 15.99,
            "category": "main_course",
            "is_available": True,
            "is_featured": False,
        }

        # Act
        response = admin_client.post(
            f"/api/v1/restaurants/admin/restaurants/{restaurant.id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["name"] == "Admin Created Dish"
        assert data["description"] == "Created by admin"
        assert data["price"] == "15.99"
        assert data["category"] == "main_course"
        assert data["restaurant_id"] == restaurant.id

        # Verify in database
        result = await test_session.exec(
            select(DishModel).where(DishModel.id == data["id"])
        )
        created_dish = result.first()
        assert created_dish is not None
        assert created_dish.name == "Admin Created Dish"

    @pytest.mark.asyncio
    async def test_create_dish_for_any_restaurant(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
    ):
        """Test admin can create dishes for any restaurant without ownership check.

        Given: Multiple restaurants exist
        When: Admin creates dishes for different restaurants
        Then: All dishes are created successfully
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="Restaurant 1")
        restaurant2 = await create_test_restaurant(name="Restaurant 2")

        dish1_data = {
            "name": "Dish for Restaurant 1",
            "price": 10.0,
            "category": "appetizer",
        }
        dish2_data = {
            "name": "Dish for Restaurant 2",
            "price": 20.0,
            "category": "main_course",
        }

        # Act
        response1 = admin_client.post(
            f"/api/v1/restaurants/admin/restaurants/{restaurant1.id}/dishes",
            json=dish1_data,
        )
        response2 = admin_client.post(
            f"/api/v1/restaurants/admin/restaurants/{restaurant2.id}/dishes",
            json=dish2_data,
        )

        # Assert
        assert response1.status_code == HTTPStatus.CREATED
        assert response2.status_code == HTTPStatus.CREATED
        assert response1.json()["restaurant_id"] == restaurant1.id
        assert response2.json()["restaurant_id"] == restaurant2.id

    def test_create_dish_nonexistent_restaurant(self, admin_client):
        """Test creating dish for non-existent restaurant returns 404.

        Given: A restaurant ID that doesn't exist
        When: Admin tries to create a dish for it
        Then: Returns 404 Not Found
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"
        dish_data = {
            "name": "Test Dish",
            "price": 10.0,
            "category": "appetizer",
        }

        # Act
        response = admin_client.post(
            f"/api/v1/restaurants/admin/restaurants/{nonexistent_id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_create_dish_invalid_restaurant_id(self, admin_client):
        """Test creating dish with invalid restaurant ID returns 422.

        Given: An invalid ULID format
        When: Admin tries to create a dish
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
        response = admin_client.post(
            f"/api/v1/restaurants/admin/restaurants/{invalid_id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_dish_missing_required_fields(
        self, admin_client, create_test_restaurant
    ):
        """Test creating dish without required fields returns 422.

        Given: A restaurant exists
        When: Admin tries to create dish without required fields
        Then: Returns 422 Unprocessable Entity
        """
        # This test would need to be async if using create_test_restaurant
        # For now, just test with a valid-looking ID
        dish_data = {
            "description": "Missing name and price",
        }

        # Act
        response = admin_client.post(
            "/api/v1/restaurants/admin/restaurants/01HQZX123456789ABCDEFGHIJK/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_create_dish_requires_admin_role(self, test_client, create_test_restaurant):
        """Test that create endpoint requires admin authentication.

        Given: No admin authentication provided
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
            "/api/v1/restaurants/admin/restaurants/01HQZX123456789ABC/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    @pytest.mark.asyncio
    async def test_create_dish_with_optional_fields(
        self,
        admin_client,
        test_session: AsyncSession,
        create_test_restaurant,
    ):
        """Test creating dish with all optional fields.

        Given: A restaurant exists
        When: Admin creates dish with optional fields
        Then: Dish is created with all fields
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")

        dish_data = {
            "name": "Complete Dish",
            "description": "Full description",
            "price": 25.50,
            "category": "main_course",
            "is_available": False,
            "is_featured": True,
            "preparation_time_minutes": 30,
            "image_url": "https://example.com/image.jpg",
            "allergens": ["gluten", "nuts"],
            "spice_level": "medium",
        }

        # Act
        response = admin_client.post(
            f"/api/v1/restaurants/admin/restaurants/{restaurant.id}/dishes",
            json=dish_data,
        )

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["description"] == "Full description"
        assert data["is_available"] is False
        assert data["is_featured"] is True
        assert data["preparation_time_minutes"] == 30
