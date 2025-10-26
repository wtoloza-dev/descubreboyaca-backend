"""E2E tests for POST /auth/refresh endpoint.

These tests verify token refresh functionality through the HTTP API.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestRefreshToken:
    """E2E tests for token refresh endpoint."""

    def test_refresh_with_valid_refresh_token(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test refresh with valid refresh token returns new access token.

        Given: User has valid refresh token from login
        When: POST /auth/refresh with refresh_token
        Then: Returns 200 with new access_token
        """
        # Arrange
        user = pytest.helpers.run_async(
            create_test_user(
                email="refresh@example.com",
                hashed_password=test_password.hashed_password,
            )
        )

        # Login to get tokens
        login_response = test_client.post(
            "/auth/login",
            json={"email": "refresh@example.com", "password": test_password.password},
        )
        refresh_token = login_response.json()["refresh_token"]

        # Act
        response = test_client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
        # JWT should have 3 parts
        assert data["access_token"].count(".") == 2

    def test_refresh_with_invalid_token(self, test_client: TestClient):
        """Test refresh with invalid token returns 401.

        Given: Invalid or malformed refresh token
        When: POST /auth/refresh
        Then: Returns 401 Unauthorized
        """
        # Arrange
        payload = {"refresh_token": "invalid.token.here"}

        # Act
        response = test_client.post("/auth/refresh", json=payload)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_with_expired_token(
        self, test_client: TestClient, create_test_user, token_provider
    ):
        """Test refresh with expired token returns 401.

        Given: Refresh token has expired
        When: POST /auth/refresh
        Then: Returns 401 Unauthorized
        """
        # Arrange
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        user = pytest.helpers.run_async(create_test_user(email="expired@example.com"))

        # Create an expired refresh token
        expired_payload = {
            "sub": user.id,
            "type": "refresh",
            "exp": datetime.now(UTC) - timedelta(days=1),  # Expired 1 day ago
            "iat": datetime.now(UTC) - timedelta(days=8),
        }
        expired_token = jwt.encode(
            expired_payload,
            token_provider.secret_key,
            algorithm=token_provider.algorithm,
        )

        # Act
        response = test_client.post(
            "/auth/refresh",
            json={"refresh_token": expired_token},
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_with_access_token_instead_of_refresh(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test refresh with access token instead of refresh token returns 401.

        Given: Using access token instead of refresh token
        When: POST /auth/refresh
        Then: Returns 401 Unauthorized (wrong token type)
        """
        # Arrange
        user = pytest.helpers.run_async(
            create_test_user(
                email="wrongtype@example.com",
                hashed_password=test_password.hashed_password,
            )
        )

        # Login to get tokens
        login_response = test_client.post(
            "/auth/login",
            json={"email": "wrongtype@example.com", "password": test_password.password},
        )
        access_token = login_response.json()["access_token"]

        # Act - try to use access token for refresh
        response = test_client.post(
            "/auth/refresh",
            json={"refresh_token": access_token},  # Wrong token type
        )

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_with_missing_token(self, test_client: TestClient):
        """Test refresh without token returns 422.

        Given: Request missing refresh_token field
        When: POST /auth/refresh
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {}  # Missing refresh_token

        # Act
        response = test_client.post("/auth/refresh", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_refresh_with_inactive_user(
        self, test_client: TestClient, create_test_user, user_repository, test_password
    ):
        """Test refresh with inactive user returns 403.

        Given: User was active but is now inactive
        When: POST /auth/refresh with valid token
        Then: Returns 403 Forbidden
        """
        # Arrange
        user = pytest.helpers.run_async(
            create_test_user(
                email="deactivated@example.com",
                hashed_password=test_password.hashed_password,
                is_active=True,
            )
        )

        # Login to get tokens
        login_response = test_client.post(
            "/auth/login",
            json={
                "email": "deactivated@example.com",
                "password": test_password.password,
            },
        )
        refresh_token = login_response.json()["refresh_token"]

        # Deactivate user after login
        pytest.helpers.run_async(user_repository.deactivate(user.id))

        # Act
        response = test_client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_refresh_returns_different_access_token(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test refresh returns a different access token than original.

        Given: Valid refresh token
        When: POST /auth/refresh
        Then: Returns new access token different from original
        """
        # Arrange
        user = pytest.helpers.run_async(
            create_test_user(
                email="newtokens@example.com",
                hashed_password=test_password.hashed_password,
            )
        )

        # Login to get original tokens
        login_response = test_client.post(
            "/auth/login",
            json={"email": "newtokens@example.com", "password": test_password.password},
        )
        original_access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]

        # Wait to ensure different timestamp (JWT uses seconds)
        import time

        time.sleep(1)

        # Act
        response = test_client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        new_access_token = data["access_token"]
        assert new_access_token != original_access_token
