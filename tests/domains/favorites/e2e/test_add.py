"""E2E tests for POST /favorites endpoint."""

from http import HTTPStatus

from ulid import ULID


class TestAddFavorite:
    """E2E tests for adding entities to favorites."""

    def test_add_favorite_success(self, user_client, mock_regular_user):
        """Test successfully adding an entity to favorites.

        Given: A user is authenticated
        When: POST /favorites with valid entity_type and entity_id
        Then: Returns 201 with created favorite
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": entity_id},
        )

        # Assert
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["user_id"] == mock_regular_user.id
        assert data["entity_type"] == "restaurant"
        assert data["entity_id"] == entity_id
        assert "id" in data
        assert "created_at" in data

    def test_add_favorite_duplicate_returns_conflict(self, user_client):
        """Test adding duplicate favorite returns 409 Conflict.

        Given: An entity is already favorited by user
        When: POST /favorites with same entity_type and entity_id
        Then: Returns 409 Conflict
        """
        # Arrange
        entity_id = str(ULID())
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": entity_id},
        )

        # Act
        response = user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": entity_id},
        )

        # Assert
        assert response.status_code == HTTPStatus.CONFLICT
        data = response.json()
        assert "already" in data["message"].lower()

    def test_add_favorite_requires_authentication(self, test_client):
        """Test adding favorite requires authentication.

        Given: No authentication token provided
        When: POST /favorites
        Then: Returns 401 Unauthorized
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = test_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": entity_id},
        )

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_add_favorite_invalid_entity_type(self, user_client):
        """Test adding favorite with invalid entity type.

        Given: A user is authenticated
        When: POST /favorites with invalid entity_type
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "invalid_type", "entity_id": entity_id},
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_add_favorite_missing_required_fields(self, user_client):
        """Test adding favorite without required fields.

        Given: A user is authenticated
        When: POST /favorites without entity_type or entity_id
        Then: Returns 422 Unprocessable Entity
        """
        # Act
        response = user_client.post("/api/v1/favorites", json={})

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_add_favorite_multiple_entity_types(self, user_client, mock_regular_user):
        """Test adding favorites for different entity types.

        Given: A user is authenticated
        When: POST /favorites with different entity types
        Then: All favorites are created successfully
        """
        # Arrange
        restaurant_id = str(ULID())
        dish_id = str(ULID())
        event_id = str(ULID())

        # Act & Assert
        response1 = user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": restaurant_id},
        )
        assert response1.status_code == HTTPStatus.CREATED

        response2 = user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": dish_id},
        )
        assert response2.status_code == HTTPStatus.CREATED

        response3 = user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "event", "entity_id": event_id},
        )
        assert response3.status_code == HTTPStatus.CREATED
