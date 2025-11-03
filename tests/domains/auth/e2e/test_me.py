"""E2E tests for GET /auth/me endpoint.

These tests verify getting current authenticated user information through HTTP API.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domains.auth.domain.enums import UserRole


class TestGetCurrentUser:
    """E2E tests for getting current user endpoint."""

    def test_get_me_with_valid_token(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test GET /auth/me with valid token returns user data.

        Given: User is authenticated with valid access token
        When: GET /auth/me with Authorization header
        Then: Returns 200 with current user data
        """
        # Arrange
        pytest.helpers.run_async(
            create_test_user(
                email="authenticated@example.com",
                hashed_password=test_password.hashed_password,
                full_name="Authenticated User",
            )
        )

        # Login to get token
        login_response = test_client.post(
            "/auth/login",
            json={
                "email": "authenticated@example.com",
                "password": test_password.password,
            },
        )
        access_token = login_response.json()["access_token"]

        # Act
        response = test_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "user" in data
        assert data["user"]["email"] == "authenticated@example.com"
        assert data["user"]["full_name"] == "Authenticated User"
        assert "hashed_password" not in data["user"]

    def test_get_me_without_token(self, test_client: TestClient):
        """Test GET /auth/me without token returns 401.

        Given: No authentication token provided
        When: GET /auth/me without Authorization header
        Then: Returns 401 Unauthorized
        """
        # Arrange & Act
        response = test_client.get("/auth/me")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_with_invalid_token(self, test_client: TestClient):
        """Test GET /auth/me with invalid token returns 401.

        Given: Invalid or malformed token
        When: GET /auth/me with invalid Authorization header
        Then: Returns 401 Unauthorized
        """
        # Arrange
        invalid_token = "invalid.token.here"

        # Act
        response = test_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {invalid_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_with_expired_token(
        self, test_client: TestClient, create_test_user, token_provider
    ):
        """Test GET /auth/me with expired token returns 401.

        Given: Token has expired
        When: GET /auth/me with expired token
        Then: Returns 401 Unauthorized
        """
        # Arrange
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        user = pytest.helpers.run_async(create_test_user(email="expired@example.com"))

        # Create an expired token
        expired_payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,  # StrEnum serializes directly
            "type": "access",
            "exp": datetime.now(UTC) - timedelta(hours=1),  # Expired 1 hour ago
            "iat": datetime.now(UTC) - timedelta(hours=2),
        }
        expired_token = jwt.encode(
            expired_payload,
            token_provider.secret_key,
            algorithm=token_provider.algorithm,
        )

        # Act
        response = test_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_includes_all_user_fields(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test GET /auth/me includes all expected user fields.

        Given: Valid authentication token
        When: GET /auth/me
        Then: Response includes all user fields except password
        """
        # Arrange
        pytest.helpers.run_async(
            create_test_user(
                email="complete@example.com",
                hashed_password=test_password.hashed_password,
                full_name="Complete User",
            )
        )

        login_response = test_client.post(
            "/auth/login",
            json={"email": "complete@example.com", "password": test_password.password},
        )
        access_token = login_response.json()["access_token"]

        # Act
        response = test_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        user_data = data["user"]
        expected_fields = [
            "id",
            "email",
            "full_name",
            "role",
            "is_active",
            "created_at",
            "auth_provider",
        ]
        for field in expected_fields:
            assert field in user_data, f"Expected field '{field}' not found"
        assert "hashed_password" not in user_data

    def test_get_me_with_admin_user(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test GET /auth/me with admin user returns correct role.

        Given: Admin user authenticated
        When: GET /auth/me
        Then: Returns user data with role="admin"
        """
        # Arrange
        pytest.helpers.run_async(
            create_test_user(
                email="admin@example.com",
                hashed_password=test_password.hashed_password,
                role=UserRole.ADMIN,
            )
        )

        login_response = test_client.post(
            "/auth/login",
            json={"email": "admin@example.com", "password": test_password.password},
        )
        access_token = login_response.json()["access_token"]

        # Act
        response = test_client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user"]["role"] == "admin"

    def test_get_me_with_malformed_authorization_header(self, test_client: TestClient):
        """Test GET /auth/me with malformed Authorization header returns 401.

        Given: Authorization header without "Bearer " prefix
        When: GET /auth/me
        Then: Returns 401 Unauthorized
        """
        # Arrange
        token = "some.jwt.token"

        # Act
        response = test_client.get(
            "/auth/me",
            headers={"Authorization": token},  # Missing "Bearer " prefix
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
