"""E2E tests for GET /restaurants/favorites endpoint.

Tests the list favorites endpoint (requires authentication).
"""

from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestListFavorites:
    """Test suite for GET /api/v1/restaurants/favorites endpoint."""

    def test_list_favorites_without_auth(self, test_client: TestClient):
        """Test accessing favorites without authentication.

        Given: No authentication token provided
        When: GET /api/v1/restaurants/favorites
        Then: Returns 401 with authentication error
        """
        # Arrange
        # (No setup needed - no authentication)

        # Act
        response = test_client.get("/api/v1/restaurants/favorites")

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        error = response.json()
        assert "error_code" in error
        assert error["error_code"] == "INVALID_TOKEN"

    def test_list_favorites_with_invalid_token(self, test_client: TestClient):
        """Test accessing favorites with invalid token.

        Given: Invalid authentication token
        When: GET /api/v1/restaurants/favorites
        Then: Returns 401 with authentication error
        """
        # Arrange
        invalid_token = "invalid_token_123"

        # Act
        response = test_client.get(
            "/api/v1/restaurants/favorites",
            headers={"Authorization": f"Bearer {invalid_token}"},
        )

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        error = response.json()
        assert "error_code" in error
        assert error["error_code"] == "INVALID_TOKEN"

    def test_list_favorites_empty(self, user_client):
        """Test listing favorites when user has no favorites.

        Given: User has no favorite restaurants
        When: GET /api/v1/restaurants/favorites
        Then: Returns 200 with empty paginated response
        """
        # Arrange
        # (No setup needed - user has no favorites)

        # Act
        response = user_client.get("/api/v1/restaurants/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 0
        assert data["pagination"]["total"] == 0
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["page_size"] == 20

    @pytest.mark.asyncio
    async def test_list_favorites_with_results(
        self, user_client, create_test_restaurant, mock_regular_user
    ):
        """Test listing user's favorite restaurants.

        Given: User has favorited multiple restaurants
        When: GET /api/v1/restaurants/favorites
        Then: Returns 200 with paginated favorite restaurants
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="Favorite 1", city="Tunja")
        restaurant2 = await create_test_restaurant(name="Favorite 2", city="Sogamoso")
        restaurant3 = await create_test_restaurant(name="Favorite 3", city="Duitama")

        # Add restaurants to favorites
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant1.id},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant2.id},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant3.id},
        )

        # Act
        response = user_client.get("/api/v1/restaurants/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3
        assert data["pagination"]["total"] == 3
        names = [r["name"] for r in data["data"]]
        assert "Favorite 1" in names
        assert "Favorite 2" in names
        assert "Favorite 3" in names

    @pytest.mark.asyncio
    async def test_list_favorites_includes_all_fields(
        self, user_client, create_test_restaurant
    ):
        """Test that response includes all expected restaurant fields.

        Given: User has a favorite restaurant with complete data
        When: GET /api/v1/restaurants/favorites
        Then: Response includes all required fields from RestaurantSchemaListItem
        """
        # Arrange
        restaurant = await create_test_restaurant(
            name="Complete Restaurant",
            description="A complete restaurant",
            address="Calle 1 #2-3",
            city="Tunja",
            state="Boyacá",
            phone="+57 300 123 4567",
            email="test@restaurant.com",
            cuisine_types=["Colombian", "Traditional"],
            price_level=2,
            features=["Outdoor Seating"],
        )

        # Add to favorites
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant.id},
        )

        # Act
        response = user_client.get("/api/v1/restaurants/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 1
        item = data["data"][0]
        # Verify all fields from RestaurantSchemaListItem
        assert "id" in item
        assert "name" in item
        assert "description" in item
        assert "city" in item
        assert "state" in item
        assert "phone" in item
        assert "location" in item
        assert "establishment_types" in item
        assert "cuisine_types" in item
        assert "price_level" in item
        assert "features" in item
        assert "tags" in item
        assert "created_at" in item
        assert "updated_at" in item
        assert item["name"] == "Complete Restaurant"
        assert item["city"] == "Tunja"

    @pytest.mark.asyncio
    async def test_list_favorites_with_pagination(
        self, user_client, create_test_restaurant
    ):
        """Test pagination works correctly for favorites.

        Given: User has 10 favorite restaurants
        When: GET /restaurants/favorites?page=2&page_size=3
        Then: Returns 3 items from page 2
        """
        # Arrange
        for i in range(10):
            restaurant = await create_test_restaurant(
                name=f"Restaurant {i:02d}", city="Tunja"
            )
            user_client.post(
                "/api/v1/favorites",
                json={"entity_type": "restaurant", "entity_id": restaurant.id},
            )

        # Act
        response = user_client.get("/api/v1/restaurants/favorites?page=2&page_size=3")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["page_size"] == 3
        assert data["pagination"]["total"] == 10

    @pytest.mark.asyncio
    async def test_list_favorites_only_returns_restaurants(
        self, user_client, create_test_restaurant
    ):
        """Test that only restaurant favorites are returned, not other entity types.

        Given: User has favorited restaurants and dishes
        When: GET /api/v1/restaurants/favorites
        Then: Returns only restaurant favorites
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="Restaurant 1", city="Tunja")
        restaurant2 = await create_test_restaurant(name="Restaurant 2", city="Sogamoso")

        # Add restaurants to favorites
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant1.id},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant2.id},
        )

        # Add a dish to favorites (should not appear in restaurant favorites)
        from ulid import ULID

        dish_id = str(ULID())
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": dish_id},
        )

        # Act
        response = user_client.get("/api/v1/restaurants/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 2
        assert data["pagination"]["total"] == 2
        # Verify all returned items are restaurants
        names = [r["name"] for r in data["data"]]
        assert "Restaurant 1" in names
        assert "Restaurant 2" in names

    @pytest.mark.asyncio
    async def test_list_favorites_ordered_by_created_at_desc(
        self, user_client, create_test_restaurant
    ):
        """Test that favorites are ordered by creation date (newest first).

        Given: User has multiple favorite restaurants added at different times
        When: GET /api/v1/restaurants/favorites
        Then: Returns favorites ordered by created_at descending
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="First Added", city="Tunja")
        restaurant2 = await create_test_restaurant(name="Second Added", city="Sogamoso")
        restaurant3 = await create_test_restaurant(name="Third Added", city="Duitama")

        # Add in sequence (most recent last)
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant1.id},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant2.id},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant3.id},
        )

        # Act
        response = user_client.get("/api/v1/restaurants/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3
        # Most recent favorite should be first
        assert data["data"][0]["name"] == "Third Added"
        assert data["data"][1]["name"] == "Second Added"
        assert data["data"][2]["name"] == "First Added"

    @pytest.mark.asyncio
    async def test_list_favorites_skips_deleted_restaurants(
        self, user_client, create_test_restaurant, test_session
    ):
        """Test that deleted restaurants don't appear in favorites list.

        Given: User has favorited restaurants, one of which gets deleted
        When: GET /api/v1/restaurants/favorites
        Then: Returns only existing restaurants (deleted one is excluded)
        """
        # Arrange
        restaurant1 = await create_test_restaurant(name="Still Exists", city="Tunja")
        restaurant2 = await create_test_restaurant(
            name="Will Be Deleted", city="Sogamoso"
        )

        # Add both to favorites
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant1.id},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant2.id},
        )

        # Delete restaurant2 from database
        await test_session.delete(restaurant2)
        await test_session.commit()

        # Act
        response = user_client.get("/api/v1/restaurants/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        # Should only return the restaurant that still exists
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == "Still Exists"
        # Note: total still reflects the favorite count, but items are filtered
        assert data["pagination"]["total"] == 2  # Favorite records still exist
