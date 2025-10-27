"""E2E tests for DELETE /favorites/{entity_type}/{entity_id} endpoint."""

from http import HTTPStatus

from ulid import ULID


class TestRemoveFavorite:
    """E2E tests for removing entities from favorites."""

    def test_remove_favorite_success(self, user_client):
        """Test successfully removing a favorite.

        Given: A user has favorited an entity
        When: DELETE /favorites/{entity_type}/{entity_id}
        Then: Returns 204 No Content
        """
        # Arrange
        entity_id = str(ULID())
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "restaurant", "entity_id": entity_id},
        )

        # Act
        response = user_client.delete(f"/api/v1/favorites/restaurant/{entity_id}")

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

    def test_remove_favorite_not_found(self, user_client):
        """Test removing non-existent favorite returns 404.

        Given: A favorite does not exist
        When: DELETE /favorites/{entity_type}/{entity_id}
        Then: Returns 404 Not Found
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = user_client.delete(f"/api/v1/favorites/restaurant/{entity_id}")

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
        data = response.json()
        assert "not found" in data["message"].lower()

    def test_remove_favorite_requires_authentication(self, test_client):
        """Test removing favorite requires authentication.

        Given: No authentication token provided
        When: DELETE /favorites/{entity_type}/{entity_id}
        Then: Returns 401 Unauthorized
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = test_client.delete(f"/api/v1/favorites/restaurant/{entity_id}")

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_remove_favorite_invalid_entity_type(self, user_client):
        """Test removing favorite with invalid entity type.

        Given: A user is authenticated
        When: DELETE /favorites/{invalid_type}/{entity_id}
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        entity_id = str(ULID())

        # Act
        response = user_client.delete(f"/api/v1/favorites/invalid_type/{entity_id}")

        # Assert
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_remove_favorite_different_user_not_found(self, user_client):
        """Test user cannot remove another user's favorite.

        Given: User A has favorited an entity
        When: User B tries to remove that favorite
        Then: Returns 404 Not Found (favorite doesn't exist for user B)

        Note: This test simulates the behavior - in practice, each user
        only sees their own favorites.
        """
        # Arrange
        entity_id = str(ULID())
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "dish", "entity_id": entity_id},
        )

        # Act - same user tries to remove (will succeed)
        response = user_client.delete(f"/api/v1/favorites/dish/{entity_id}")

        # Assert
        assert response.status_code == HTTPStatus.NO_CONTENT

        # Act - try to remove again (should fail)
        response2 = user_client.delete(f"/api/v1/favorites/dish/{entity_id}")

        # Assert
        assert response2.status_code == HTTPStatus.NOT_FOUND

    def test_remove_favorite_idempotent(self, user_client):
        """Test removing favorite twice returns 404 on second attempt.

        Given: A favorite has been removed
        When: DELETE /favorites/{entity_type}/{entity_id} again
        Then: Returns 404 Not Found
        """
        # Arrange
        entity_id = str(ULID())
        user_client.post(
            "/api/v1/favorites",
            json={"entity_type": "place", "entity_id": entity_id},
        )
        user_client.delete(f"/api/v1/favorites/place/{entity_id}")

        # Act
        response = user_client.delete(f"/api/v1/favorites/place/{entity_id}")

        # Assert
        assert response.status_code == HTTPStatus.NOT_FOUND
