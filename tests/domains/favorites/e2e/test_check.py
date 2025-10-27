"""E2E tests for GET /favorites/{entity_type}/{entity_id}/is-favorite endpoint."""

from http import HTTPStatus

from ulid import ULID


class TestCheckFavorite:
    """E2E tests for checking if entity is favorited."""

    def test_check_favorite_exists(self, user_client):
        """Test checking favorite that exists.

        Given: User has favorited an entity
        When: GET /favorites/{entity_type}/{entity_id}/is-favorite
        Then: Returns 200 with is_favorite=true and favorite_id
        """
        # Arrange
        entity_id = str(ULID())
        add_response = user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": entity_id},
        )
        favorite_id = add_response.json()["id"]

        # Act
        response = user_client.get(
            f"/api/v1/favorites/restaurant/{entity_id}/is-favorite"
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["is_favorite"] is True
        assert data["favorite_id"] == favorite_id

    def test_check_favorite_not_exists(self, user_client):
        """Test checking favorite that doesn't exist.

        Given: User has not favorited an entity
        When: GET /favorites/{entity_type}/{entity_id}/is-favorite
        Then: Returns 200 with is_favorite=false and favorite_id=null
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = user_client.get(
            f"/api/v1/favorites/restaurant/{entity_id}/is-favorite"
        )

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["is_favorite"] is False
        assert data["favorite_id"] is None

    def test_check_favorite_requires_authentication(self, test_client):
        """Test checking favorite requires authentication.

        Given: No authentication token provided
        When: GET /favorites/{entity_type}/{entity_id}/is-favorite
        Then: Returns 401 Unauthorized
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = test_client.get(
            f"/api/v1/favorites/restaurant/{entity_id}/is-favorite"
        )

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_check_favorite_invalid_entity_type(self, user_client):
        """Test checking favorite with invalid entity type.

        Given: A user is authenticated
        When: GET /favorites/{invalid_type}/{entity_id}/is-favorite
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = user_client.get(
            f"/api/v1/favorites/invalid_type/{entity_id}/is-favorite"
        )

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_check_favorite_after_removal(self, user_client):
        """Test checking favorite after it has been removed.

        Given: User favorited and then removed an entity
        When: GET /favorites/{entity_type}/{entity_id}/is-favorite
        Then: Returns 200 with is_favorite=false
        """
        # Arrange
        entity_id = str(ULID())
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": entity_id},
        )
        user_client.delete(f"/api/v1/favorites/dish/{entity_id}")

        # Act
        response = user_client.get(f"/api/v1/favorites/dish/{entity_id}/is-favorite")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["is_favorite"] is False
        assert data["favorite_id"] is None

    def test_check_favorite_different_entity_types(self, user_client):
        """Test checking favorites for different entity types.

        Given: User has favorited a restaurant but not a dish with same ID
        When: Checking both entity types
        Then: Returns correct is_favorite status for each
        """
        # Arrange
        entity_id = str(ULID())
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": entity_id},
        )

        # Act
        restaurant_response = user_client.get(
            f"/api/v1/favorites/restaurant/{entity_id}/is-favorite"
        )
        dish_response = user_client.get(
            f"/api/v1/favorites/dish/{entity_id}/is-favorite"
        )

        # Assert
        assert restaurant_response.status_code == HTTPStatus.OK
        assert restaurant_response.json()["is_favorite"] is True

        assert dish_response.status_code == HTTPStatus.OK
        assert dish_response.json()["is_favorite"] is False
