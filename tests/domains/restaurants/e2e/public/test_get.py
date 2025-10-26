"""E2E tests for GET /restaurants/{restaurant_id} endpoint.

Tests the get single restaurant endpoint.
"""

from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestGetRestaurant:
    """Test suite for GET /api/v1/restaurants/{restaurant_id} endpoint."""

    @pytest.mark.asyncio
    async def test_get_existing_restaurant(self, test_client: TestClient, test_session):
        """Test getting an existing restaurant.

        Given: A restaurant exists in the database
        When: GET /api/v1/restaurants/{id}
        Then: Returns 200 with restaurant data
        """
        # Arrange
        from app.domains.restaurants.models import RestaurantModel
        from app.shared.domain.factories import generate_ulid

        restaurant = RestaurantModel(
            id=generate_ulid(),
            name="Test Restaurant",
            address="Test Address",
            city="Tunja",
            state="Boyacá",
            country="Colombia",
            phone="+57 300 123 4567",
            cuisine_types=[],
            features=[],
        )
        test_session.add(restaurant)
        await test_session.flush()

        # Act
        response = test_client.get(f"/api/v1/restaurants/{restaurant.id}")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["id"] == restaurant.id
        assert data["name"] == "Test Restaurant"
        assert data["city"] == "Tunja"
        assert data["phone"] == "+57 300 123 4567"

    def test_get_nonexistent_restaurant(self, test_client: TestClient):
        """Test getting a restaurant that doesn't exist.

        Given: Valid ULID that doesn't exist in database
        When: GET /api/v1/restaurants/{id}
        Then: Returns 404 with error details
        """
        # Arrange
        nonexistent_id = "01K8E0Z3SRNDMSZPN91V7A64T3"  # Valid ULID format

        # Act
        response = test_client.get(f"/api/v1/restaurants/{nonexistent_id}")

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        error = response.json()
        assert "error_code" in error
        assert error["error_code"] == "RESTAURANT_NOT_FOUND"
        assert "message" in error

    def test_get_with_invalid_id_format(self, test_client: TestClient):
        """Test getting a restaurant with invalid ULID format.

        Given: Invalid ULID format
        When: GET /api/v1/restaurants/{id}
        Then: Returns 422 with validation error
        """
        # Arrange
        invalid_ids = [
            "invalid",  # Too short
            "01HQZX_INVALID_FORMAT_HERE",  # Invalid characters
            "abc123",  # Too short and invalid
            "01HQZXABCDEFGHIJKLMNOPQRSTU",  # 27 chars (too long)
        ]

        # Act & Assert
        for invalid_id in invalid_ids:
            response = test_client.get(f"/api/v1/restaurants/{invalid_id}")
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_get_restaurant_includes_all_fields(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test that response includes all fields.

        Given: A restaurant with complete data
        When: GET /api/v1/restaurants/{id}
        Then: Response includes all fields
        """
        # Arrange
        restaurant = await create_test_restaurant(
            name="Complete Restaurant",
            description="A complete restaurant",
            address="Calle 1 #2-3",
            city="Tunja",
            phone="+57 300 123 4567",
            email="test@restaurant.com",
            website="https://restaurant.com",
        )

        # Act
        response = test_client.get(f"/api/v1/restaurants/{restaurant.id}")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["name"] == "Complete Restaurant"
        assert data["description"] == "A complete restaurant"
        assert data["address"] == "Calle 1 #2-3"
        assert data["email"] == "test@restaurant.com"
        assert data["website"] == "https://restaurant.com/"  # Pydantic normalizes URLs
