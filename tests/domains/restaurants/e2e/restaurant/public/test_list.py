"""E2E tests for GET /restaurants/ endpoint.

Tests the list all restaurants endpoint with pagination.
"""

from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestListRestaurants:
    """Test suite for GET /api/v1/restaurants/ endpoint."""

    def test_list_empty(self, test_client: TestClient):
        """Test listing restaurants when database is empty.

        Given: No restaurants in the database
        When: GET /api/v1/restaurants/
        Then: Returns 200 with empty paginated response
        """
        # Arrange
        # (No setup needed - empty database)

        # Act
        response = test_client.get("/api/v1/restaurants/")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 0
        assert data["pagination"]["total"] == 0

    @pytest.mark.asyncio
    async def test_list_with_restaurants(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test listing multiple restaurants.

        Given: Multiple restaurants in the database
        When: GET /api/v1/restaurants/
        Then: Returns 200 with paginated restaurants
        """
        # Arrange
        await create_test_restaurant(name="Restaurant 1", city="Tunja")
        await create_test_restaurant(name="Restaurant 2", city="Sogamoso")
        await create_test_restaurant(name="Restaurant 3", city="Duitama")

        # Act
        response = test_client.get("/api/v1/restaurants/")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3
        assert data["pagination"]["total"] == 3
        names = [r["name"] for r in data["data"]]
        assert "Restaurant 1" in names
        assert "Restaurant 2" in names
        assert "Restaurant 3" in names

    @pytest.mark.asyncio
    async def test_list_includes_all_fields(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test that response includes all expected fields.

        Given: A restaurant with complete data
        When: GET /api/v1/restaurants/
        Then: Response includes all required fields
        """
        # Arrange
        await create_test_restaurant(
            name="Complete Restaurant",
            description="A complete restaurant",
            address="Calle 1 #2-3",
            city="Tunja",
            phone="+57 300 123 4567",
            email="test@restaurant.com",
        )

        # Act
        response = test_client.get("/api/v1/restaurants/")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 1
        assert data["pagination"]["total"] == 1
        restaurant = data["data"][0]
        # Verify fields from RestaurantListItem schema (summary view)
        assert "id" in restaurant
        assert "name" in restaurant
        assert "description" in restaurant
        assert "city" in restaurant
        assert "state" in restaurant
        assert "phone" in restaurant
        assert "cuisine_types" in restaurant
        assert "price_level" in restaurant
        assert "features" in restaurant
        assert "created_at" in restaurant
        assert "updated_at" in restaurant
        # Note: 'address' and 'email' are NOT in RestaurantListItem

    @pytest.mark.asyncio
    async def test_list_with_pagination(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test pagination works correctly.

        Given: 15 restaurants in database
        When: GET /restaurants?page=2&page_size=5
        Then: Returns 5 items from page 2
        """
        # Arrange
        for i in range(15):
            await create_test_restaurant(name=f"Restaurant {i:02d}", city="Tunja")

        # Act
        response = test_client.get("/api/v1/restaurants/?page=2&page_size=5")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 5
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["page_size"] == 5
        assert data["pagination"]["total"] == 15

    @pytest.mark.asyncio
    async def test_list_filter_by_city(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test filtering by city.

        Given: Restaurants in different cities
        When: GET /restaurants?city=Tunja
        Then: Returns only Tunja restaurants
        """
        # Arrange
        await create_test_restaurant(name="Tunja 1", city="Tunja")
        await create_test_restaurant(name="Tunja 2", city="Tunja")
        await create_test_restaurant(name="Sogamoso 1", city="Sogamoso")

        # Act
        response = test_client.get("/api/v1/restaurants/?city=Tunja")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["pagination"]["total"] == 2
        assert len(data["data"]) == 2
        assert all(r["city"] == "Tunja" for r in data["data"])

    @pytest.mark.asyncio
    async def test_list_filter_by_price_level(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test filtering by price level.

        Given: Restaurants with different price levels
        When: GET /restaurants?price_level=2
        Then: Returns only price_level=2 restaurants
        """
        # Arrange
        await create_test_restaurant(name="Budget", city="Tunja", price_level=1)
        await create_test_restaurant(name="Moderate 1", city="Tunja", price_level=2)
        await create_test_restaurant(name="Moderate 2", city="Tunja", price_level=2)
        await create_test_restaurant(name="Expensive", city="Tunja", price_level=3)

        # Act
        response = test_client.get("/api/v1/restaurants/?price_level=2")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["pagination"]["total"] == 2
        assert len(data["data"]) == 2
        assert all(r["price_level"] == 2 for r in data["data"])

    @pytest.mark.asyncio
    async def test_list_filter_combined(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test combining multiple filters.

        Given: Restaurants with various attributes
        When: GET /restaurants?city=Tunja&price_level=2
        Then: Returns only matching restaurants
        """
        # Arrange
        await create_test_restaurant(name="Match Both", city="Tunja", price_level=2)
        await create_test_restaurant(name="Wrong City", city="Sogamoso", price_level=2)
        await create_test_restaurant(name="Wrong Price", city="Tunja", price_level=1)
        await create_test_restaurant(name="Wrong Both", city="Duitama", price_level=3)

        # Act
        response = test_client.get("/api/v1/restaurants/?city=Tunja&price_level=2")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["pagination"]["total"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == "Match Both"
        assert data["data"][0]["city"] == "Tunja"
        assert data["data"][0]["price_level"] == 2

    @pytest.mark.asyncio
    async def test_list_pagination_large_page_size(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test that page_size has a reasonable maximum limit.

        Given: Request with extremely large page_size
        When: GET /restaurants?page_size=99999
        Then: Returns success with capped page_size or validation error
        """
        # Arrange
        for i in range(5):
            await create_test_restaurant(name=f"Restaurant {i}")

        # Act
        response = test_client.get("/api/v1/restaurants/?page_size=99999")

        # Assert
        assert response.status_code in [HTTPStatus.OK, HTTPStatus.UNPROCESSABLE_ENTITY]
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            assert data["pagination"]["page_size"] <= 100, (
                "page_size should be capped to prevent DoS"
            )
