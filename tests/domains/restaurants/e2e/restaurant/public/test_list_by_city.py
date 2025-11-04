"""E2E tests for GET /restaurants/city/{city} endpoint.

Tests the list restaurants by city endpoint with pagination.
"""

from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestListRestaurantsByCity:
    """Test suite for GET /api/v1/restaurants/city/{city} endpoint."""

    @pytest.mark.asyncio
    async def test_list_by_city_with_results(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test listing restaurants in a specific city.

        Given: Multiple restaurants in different cities
        When: GET /api/v1/restaurants/city/{city}
        Then: Returns paginated restaurants from that city only
        """
        # Arrange
        await create_test_restaurant(name="Tunja Restaurant 1", city="Tunja")
        await create_test_restaurant(name="Tunja Restaurant 2", city="Tunja")
        await create_test_restaurant(name="Sogamoso Restaurant", city="Sogamoso")

        # Act
        response = test_client.get("/api/v1/restaurants/city/Tunja")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) == 2
        assert data["pagination"]["total"] == 2
        assert all(r["city"] == "Tunja" for r in data["data"])
        names = [r["name"] for r in data["data"]]
        assert "Tunja Restaurant 1" in names
        assert "Tunja Restaurant 2" in names

    def test_list_by_city_empty(self, test_client: TestClient):
        """Test listing restaurants in city with no restaurants.

        Given: No restaurants in the specified city
        When: GET /api/v1/restaurants/city/{city}
        Then: Returns 200 with empty paginated response
        """
        # Arrange
        # (No setup needed - empty database)

        # Act
        response = test_client.get("/api/v1/restaurants/city/Duitama")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 0
        assert data["pagination"]["total"] == 0

    @pytest.mark.asyncio
    async def test_list_by_city_case_sensitive(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test that city filtering is case-sensitive.

        Given: Restaurants with city "Tunja"
        When: GET /api/v1/restaurants/city/tunja (lowercase)
        Then: Returns empty paginated response (case-sensitive)
        """
        # Arrange
        await create_test_restaurant(name="Tunja Restaurant", city="Tunja")

        # Act
        response = test_client.get("/api/v1/restaurants/city/tunja")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 0
        assert data["pagination"]["total"] == 0

    @pytest.mark.asyncio
    async def test_list_by_city_with_pagination(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test pagination in city filter.

        Given: 10 restaurants in Tunja
        When: GET /city/Tunja?page=2&page_size=3
        Then: Returns page 2 with 3 items
        """
        # Arrange
        for i in range(10):
            await create_test_restaurant(name=f"Tunja Restaurant {i:02d}", city="Tunja")

        # Act
        response = test_client.get("/api/v1/restaurants/city/Tunja?page=2&page_size=3")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["page_size"] == 3
        assert data["pagination"]["total"] == 10
        assert all(r["city"] == "Tunja" for r in data["data"])

    @pytest.mark.asyncio
    async def test_list_by_city_with_spaces(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test city names with spaces.

        Given: Restaurant in "Villa de Leyva"
        When: GET /city/Villa%20de%20Leyva
        Then: Returns restaurant correctly
        """
        # Arrange
        await create_test_restaurant(
            name="Villa Restaurant", city="Villa de Leyva", address="Calle 1 #2-3"
        )

        # Act
        response = test_client.get("/api/v1/restaurants/city/Villa%20de%20Leyva")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["pagination"]["total"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["city"] == "Villa de Leyva"
        assert data["data"][0]["name"] == "Villa Restaurant"

    @pytest.mark.asyncio
    async def test_list_by_city_with_accents(
        self, test_client: TestClient, create_test_restaurant
    ):
        """Test city names with accents.

        Given: Restaurant in "Bogotá"
        When: GET /city/Bogotá (URL encoded)
        Then: Returns restaurant correctly
        """
        # Arrange
        await create_test_restaurant(
            name="Bogotá Restaurant", city="Bogotá", address="Carrera 7 #12-34"
        )

        # Act
        response = test_client.get("/api/v1/restaurants/city/Bogot%C3%A1")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["pagination"]["total"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["city"] == "Bogotá"
        assert data["data"][0]["name"] == "Bogotá Restaurant"
