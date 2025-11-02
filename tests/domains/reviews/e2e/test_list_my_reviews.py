"""E2E tests for GET /reviews/me endpoint."""

from http import HTTPStatus


class TestListMyReviews:
    """E2E tests for listing user's reviews."""

    def test_list_my_reviews_empty(self, user_client):
        """Test listing reviews when user has none.

        Given: User has no reviews
        When: GET /reviews/me
        Then: Returns 200 with empty list
        """
        # Act
        response = user_client.get("/api/v1/reviews/me")

        # Assert
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 20

    def test_list_my_reviews_requires_authentication(self, test_client):
        """Test listing reviews requires authentication.

        Given: No authentication token provided
        When: GET /reviews/me
        Then: Returns 401 Unauthorized
        """
        # Act
        response = test_client.get("/api/v1/reviews/me")

        # Assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    # NOTE: Additional E2E tests (pagination, filtering, etc.) will be added
    # when we implement the POST /reviews endpoint to create reviews via HTTP
