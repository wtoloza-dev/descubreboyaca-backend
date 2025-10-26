"""E2E tests for GET /restaurants/favorites endpoint.

Tests the list favorites endpoint (requires authentication).
"""

from http import HTTPStatus

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
