"""E2E tests for GET /restaurants/dishes/{dish_id} endpoint.

This module tests the public endpoint for retrieving a single dish by its ID.
"""

from decimal import Decimal

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.shared.domain.factories import generate_ulid


class TestGetDish:
    """E2E tests for GET /restaurants/dishes/{dish_id} endpoint."""

    @pytest.mark.asyncio
    async def test_get_existing_dish(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test getting an existing dish returns 200 with complete data.

        Given: A dish exists in the database
        When: Making GET request to /restaurants/dishes/{dish_id}
        Then: Returns 200 OK with complete dish information
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Ajiaco Santafereño",
            description="Traditional Colombian soup",
            category="main_course",
            price=Decimal("25000.00"),
            is_available=True,
        )

        # Act
        response = test_client.get(f"/api/v1/restaurants/dishes/{dish.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == dish.id
        assert data["name"] == "Ajiaco Santafereño"
        assert data["description"] == "Traditional Colombian soup"
        assert data["category"] == "main_course"
        assert data["price"] == "25000.00"
        assert data["is_available"] is True

    @pytest.mark.asyncio
    async def test_get_nonexistent_dish(self, test_client: TestClient):
        """Test getting a non-existent dish returns 404.

        Given: A dish ID that doesn't exist in the database
        When: Making GET request to /restaurants/dishes/{dish_id}
        Then: Returns 404 NOT FOUND
        """
        # Arrange
        nonexistent_id = generate_ulid()

        # Act
        response = test_client.get(f"/api/v1/restaurants/dishes/{nonexistent_id}")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        # The API returns structured error response with message field
        assert "message" in data or "detail" in data

    def test_get_with_invalid_id_format(self, test_client: TestClient):
        """Test getting a dish with invalid ULID format returns 422.

        Given: An invalid ULID format
        When: Making GET request to /restaurants/dishes/{invalid_id}
        Then: Returns 422 UNPROCESSABLE ENTITY
        """
        # Arrange
        invalid_id = "invalid-ulid-format"

        # Act
        response = test_client.get(f"/api/v1/restaurants/dishes/{invalid_id}")

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_get_dish_includes_all_fields(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test getting a dish returns all expected fields in response.

        Given: A dish with complete data exists
        When: Making GET request to /restaurants/dishes/{dish_id}
        Then: Response includes all dish fields (name, price, category, etc.)
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Bandeja Paisa",
            description="Traditional Colombian platter",
            category="main_course",
            price=Decimal("35000.00"),
            original_price=Decimal("40000.00"),
            is_available=True,
            preparation_time_minutes=60,
            serves=1,
            calories=1200,
            dietary_restrictions=["gluten_free"],
            ingredients=["beans", "rice", "meat", "chorizo", "egg"],
            allergens=["egg"],
            flavor_profile={"savory": "high", "hearty": "extreme"},
            is_featured=True,
            display_order=1,
        )

        # Act
        response = test_client.get(f"/api/v1/restaurants/dishes/{dish.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify all expected fields are present
        assert "id" in data
        assert "restaurant_id" in data
        assert "name" in data
        assert "description" in data
        assert "category" in data
        assert "price" in data
        assert "original_price" in data
        assert "is_available" in data
        assert "preparation_time_minutes" in data
        assert "serves" in data
        assert "calories" in data
        assert "dietary_restrictions" in data
        assert "ingredients" in data
        assert "allergens" in data
        assert "flavor_profile" in data
        assert "is_featured" in data
        assert "display_order" in data
        # Audit fields (inherited from Audit)
        assert "created_at" in data
        assert "updated_at" in data

        # Verify specific values
        assert data["name"] == "Bandeja Paisa"
        assert data["price"] == "35000.00"
        assert data["original_price"] == "40000.00"
        assert data["dietary_restrictions"] == ["gluten_free"]
        assert data["flavor_profile"] == {"savory": "high", "hearty": "extreme"}

    @pytest.mark.asyncio
    async def test_get_dish_with_minimal_data(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test getting a dish with minimal required fields only.

        Given: A dish exists with only required fields
        When: Making GET request to /restaurants/dishes/{dish_id}
        Then: Returns 200 OK with null/empty optional fields
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        dish = await create_test_dish(
            restaurant_id=restaurant.id,
            name="Simple Dish",
            description=None,
            category="dessert",
            price=Decimal("8000.00"),
            original_price=None,
            preparation_time_minutes=None,
            serves=None,
            calories=None,
            image_url=None,
            dietary_restrictions=[],
            ingredients=[],
            allergens=[],
            flavor_profile={},
        )

        # Act
        response = test_client.get(f"/api/v1/restaurants/dishes/{dish.id}")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Simple Dish"
        assert data["description"] is None
        assert data["original_price"] is None
        assert data["preparation_time_minutes"] is None
        assert data["dietary_restrictions"] == []
        assert data["ingredients"] == []
        assert data["flavor_profile"] == {}
