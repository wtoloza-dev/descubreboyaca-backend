"""E2E tests for GET /restaurants/{restaurant_id}/dishes endpoint.

This module tests the public endpoint for listing dishes of a restaurant.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.shared.domain.factories import generate_ulid


class TestListRestaurantDishes:
    """E2E tests for GET /restaurants/{restaurant_id}/dishes endpoint."""

    @pytest.mark.asyncio
    async def test_list_dishes_with_results(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test listing dishes for a restaurant returns paginated results.

        Given: A restaurant with multiple dishes exists
        When: Making GET request to /restaurants/{id}/dishes
        Then: Returns 200 OK with paginated list of dishes
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Dish 1",
            category="appetizer",
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Dish 2",
            category="main_course",
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Dish 3",
            category="dessert",
        )

        # Act
        response = test_client.get(f"/api/v1/restaurants/{restaurant.id}/dishes/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert "page" in data["pagination"]
        assert "page_size" in data["pagination"]
        assert "total" in data["pagination"]
        assert len(data["data"]) == 3
        assert data["pagination"]["total"] == 3

    @pytest.mark.asyncio
    async def test_list_dishes_empty(
        self,
        test_client: TestClient,
        create_test_restaurant,
    ):
        """Test listing dishes for a restaurant with no dishes returns empty list.

        Given: A restaurant exists with no dishes
        When: Making GET request to /restaurants/{id}/dishes
        Then: Returns 200 OK with empty items list and total 0
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Empty Restaurant")

        # Act
        response = test_client.get(f"/api/v1/restaurants/{restaurant.id}/dishes/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"] == []
        assert data["pagination"]["total"] == 0

    @pytest.mark.asyncio
    async def test_list_dishes_nonexistent_restaurant(self, test_client: TestClient):
        """Test listing dishes for non-existent restaurant returns 404.

        Given: A restaurant ID that doesn't exist
        When: Making GET request to /restaurants/{id}/dishes
        Then: Returns 404 NOT FOUND
        """
        # Arrange
        nonexistent_id = generate_ulid()

        # Act
        response = test_client.get(f"/api/v1/restaurants/{nonexistent_id}/dishes/")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        # The API returns structured error response with message field
        assert "message" in data or "detail" in data

    def test_list_dishes_invalid_restaurant_id_format(self, test_client: TestClient):
        """Test listing dishes with invalid restaurant ULID format returns 422.

        Given: An invalid ULID format
        When: Making GET request to /restaurants/{invalid_id}/dishes
        Then: Returns 422 UNPROCESSABLE ENTITY
        """
        # Arrange
        invalid_id = "not-a-valid-ulid"

        # Act
        response = test_client.get(f"/api/v1/restaurants/{invalid_id}/dishes/")

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    @pytest.mark.asyncio
    async def test_list_dishes_with_pagination(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test listing dishes with pagination parameters.

        Given: A restaurant with 10 dishes exists
        When: Requesting page 2 with page_size 3
        Then: Returns 3 dishes from page 2 with correct pagination metadata
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        for i in range(10):
            await create_test_dish(
                restaurant_id=restaurant.id,
                name=f"Dish {i:02d}",
                display_order=i,
            )

        # Act
        response = test_client.get(
            f"/api/v1/restaurants/{restaurant.id}/dishes/?page=2&page_size=3"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 3
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["page_size"] == 3
        assert data["pagination"]["total"] == 10

    @pytest.mark.asyncio
    async def test_list_dishes_filter_by_category(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test filtering dishes by category.

        Given: A restaurant with dishes in multiple categories
        When: Requesting dishes filtered by category=dessert
        Then: Returns only dessert dishes
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Appetizer 1",
            category="appetizer",
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Dessert 1",
            category="dessert",
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Dessert 2",
            category="dessert",
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Main Course 1",
            category="main_course",
        )

        # Act
        response = test_client.get(
            f"/api/v1/restaurants/{restaurant.id}/dishes/?category=dessert"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 2
        assert data["pagination"]["total"] == 2
        assert all(dish["category"] == "dessert" for dish in data["data"])

    @pytest.mark.asyncio
    async def test_list_dishes_filter_by_availability(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test filtering dishes by availability.

        Given: A restaurant with available and unavailable dishes
        When: Requesting dishes filtered by is_available=true
        Then: Returns only available dishes
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Available Dish 1",
            is_available=True,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Available Dish 2",
            is_available=True,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Unavailable Dish",
            is_available=False,
        )

        # Act
        response = test_client.get(
            f"/api/v1/restaurants/{restaurant.id}/dishes/?is_available=true"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 2
        assert data["pagination"]["total"] == 2
        assert all(dish["is_available"] is True for dish in data["data"])

    @pytest.mark.asyncio
    async def test_list_dishes_filter_by_featured(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test filtering dishes by featured status.

        Given: A restaurant with featured and non-featured dishes
        When: Requesting dishes filtered by is_featured=true
        Then: Returns only featured dishes
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Featured Dish",
            is_featured=True,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Regular Dish 1",
            is_featured=False,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Regular Dish 2",
            is_featured=False,
        )

        # Act
        response = test_client.get(
            f"/api/v1/restaurants/{restaurant.id}/dishes/?is_featured=true"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 1
        assert data["pagination"]["total"] == 1
        assert data["data"][0]["is_featured"] is True

    @pytest.mark.asyncio
    async def test_list_dishes_multiple_filters(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test combining multiple filters.

        Given: A restaurant with various dishes
        When: Requesting with category=dessert and is_available=true
        Then: Returns only available desserts
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Available Dessert",
            category="dessert",
            is_available=True,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Unavailable Dessert",
            category="dessert",
            is_available=False,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Available Main",
            category="main_course",
            is_available=True,
        )

        # Act
        response = test_client.get(
            f"/api/v1/restaurants/{restaurant.id}/dishes/?category=dessert&is_available=true"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 1
        assert data["pagination"]["total"] == 1
        assert data["data"][0]["category"] == "dessert"
        assert data["data"][0]["is_available"] is True

    @pytest.mark.asyncio
    async def test_list_dishes_ordering(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test dishes are ordered by display_order and then by name.

        Given: A restaurant with dishes having different display orders
        When: Requesting all dishes
        Then: Returns dishes sorted by display_order (ascending), then name
        """
        # Arrange
        restaurant = await create_test_restaurant(name="Test Restaurant")
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Zebra Dish",
            display_order=2,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Apple Dish",
            display_order=1,
        )
        await create_test_dish(
            restaurant_id=restaurant.id,
            name="Banana Dish",
            display_order=1,
        )

        # Act
        response = test_client.get(f"/api/v1/restaurants/{restaurant.id}/dishes/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        items = data["data"]
        assert len(items) == 3

        # Should be sorted by display_order first, then by name
        assert items[0]["name"] == "Apple Dish"  # display_order=1, name=A
        assert items[1]["name"] == "Banana Dish"  # display_order=1, name=B
        assert items[2]["name"] == "Zebra Dish"  # display_order=2

    @pytest.mark.asyncio
    async def test_list_dishes_only_returns_dishes_from_specified_restaurant(
        self,
        test_client: TestClient,
        create_test_restaurant,
        create_test_dish,
    ):
        """Test that listing dishes only returns dishes from the specified restaurant.

        Given: Two restaurants with their own dishes
        When: Requesting dishes for restaurant 1
        Then: Returns only dishes from restaurant 1, not restaurant 2
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="Restaurant 1")
        restaurant2 = await create_test_restaurant(name="Restaurant 2")

        await create_test_dish(
            restaurant_id=restaurant1.id,
            name="R1 Dish 1",
        )
        await create_test_dish(
            restaurant_id=restaurant1.id,
            name="R1 Dish 2",
        )
        await create_test_dish(
            restaurant_id=restaurant2.id,
            name="R2 Dish 1",
        )

        # Act
        response = test_client.get(f"/api/v1/restaurants/{restaurant1.id}/dishes/")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["data"]) == 2
        assert data["pagination"]["total"] == 2
        assert all(dish["restaurant_id"] == restaurant1.id for dish in data["data"])
        assert all("R1" in dish["name"] for dish in data["data"])
