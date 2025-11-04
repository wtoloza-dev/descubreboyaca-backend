"""E2E tests for GET /favorites endpoint."""

from http import HTTPStatus

from ulid import ULID


class TestListFavorites:
    """E2E tests for listing user's favorites."""

    def test_list_favorites_empty(self, user_client):
        """Test listing favorites when user has none.

        Given: User has no favorites
        When: GET /favorites
        Then: Returns 200 with empty list
        """
        # Act
        response = user_client.get("/api/v1/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["data"] == []
        assert data["pagination"]["total"] == 0
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["page_size"] == 20

    def test_list_favorites_with_results(self, user_client, mock_regular_user):
        """Test listing favorites with multiple items.

        Given: User has favorited multiple entities
        When: GET /favorites
        Then: Returns 200 with all favorites
        """
        # Arrange
        restaurant_id = str(ULID())
        dish_id = str(ULID())
        event_id = str(ULID())

        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant_id},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": dish_id},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "event", "entity_id": event_id},
        )

        # Act
        response = user_client.get("/api/v1/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3
        assert data["pagination"]["total"] == 3
        assert all(item["user_id"] == mock_regular_user.id for item in data["data"])

    def test_list_favorites_filter_by_entity_type(self, user_client):
        """Test filtering favorites by entity type.

        Given: User has favorites of different types
        When: GET /favorites?entity_type=restaurant
        Then: Returns only restaurant favorites
        """
        # Arrange
        restaurant_id1 = str(ULID())
        restaurant_id2 = str(ULID())
        dish_id = str(ULID())

        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant_id1},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant_id2},
        )
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": dish_id},
        )

        # Act
        response = user_client.get("/api/v1/favorites?entity_type=restaurant")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 2
        assert data["pagination"]["total"] == 2
        assert all(item["entity_type"] == "restaurant" for item in data["data"])

    def test_list_favorites_with_pagination(self, user_client):
        """Test listing favorites with pagination.

        Given: User has 5 favorites
        When: GET /favorites?page=2&page_size=2
        Then: Returns page 2 with 2 items
        """
        # Arrange
        for i in range(5):
            entity_id = str(ULID())
            user_client.post(
                "/api/v1/favorites",
                json={"entity_type": "restaurant", "entity_id": entity_id},
            )

        # Act
        response = user_client.get("/api/v1/favorites?page=2&page_size=2")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 2
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["page_size"] == 2
        assert data["pagination"]["total"] == 5

    def test_list_favorites_requires_authentication(self, test_client):
        """Test listing favorites requires authentication.

        Given: No authentication token provided
        When: GET /favorites
        Then: Returns 401 Unauthorized
        """
        # Act
        response = test_client.get("/api/v1/favorites")

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_list_favorites_ordered_by_created_at_desc(self, user_client):
        """Test favorites are ordered by created_at descending.

        Given: User has multiple favorites created at different times
        When: GET /favorites
        Then: Returns favorites ordered by created_at (newest first)
        """
        # Arrange
        entity_ids = [str(ULID()) for _ in range(3)]
        for entity_id in entity_ids:
            user_client.post(
                "/api/v1/favorites",
                json={"entity_type": "restaurant", "entity_id": entity_id},
            )

        # Act
        response = user_client.get("/api/v1/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 3

        # Verify ordering (newest first)
        created_dates = [item["created_at"] for item in data["data"]]
        assert created_dates == sorted(created_dates, reverse=True)

    def test_list_favorites_includes_all_fields(self, user_client, mock_regular_user):
        """Test response includes all expected fields.

        Given: User has a favorite
        When: GET /favorites
        Then: Each item includes id, user_id, entity_type, entity_id, created_at
        """
        # Arrange
        entity_id = str(ULID())
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": entity_id},
        )

        # Act
        response = user_client.get("/api/v1/favorites")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data["data"]) == 1

        item = data["data"][0]
        assert "id" in item
        assert "user_id" in item
        assert "entity_type" in item
        assert "entity_id" in item
        assert "created_at" in item
        assert item["user_id"] == mock_regular_user.id
        assert item["entity_type"] == "dish"
        assert item["entity_id"] == entity_id
