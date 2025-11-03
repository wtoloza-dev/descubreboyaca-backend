"""E2E tests for POST /auth/login endpoint.

These tests verify user authentication through the HTTP API.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.domains.auth.domain.enums import UserRole


class TestLoginUser:
    """E2E tests for user login endpoint."""

    def test_login_with_valid_credentials(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test login with valid credentials returns 200 with tokens.

        Given: User exists with email and password
        When: POST /auth/login with correct credentials
        Then: Returns 200 with access_token, refresh_token, and user data
        """
        # Arrange
        pytest.helpers.run_async(
            create_test_user(
                email="testuser@example.com",
                hashed_password=test_password.hashed_password,
                full_name="Test User",
            )
        )

        payload = {"email": "testuser@example.com", "password": test_password.password}

        # Act
        response = test_client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "testuser@example.com"
        assert data["user"]["full_name"] == "Test User"
        assert "hashed_password" not in data["user"]  # Should not expose password

    def test_login_with_invalid_email(self, test_client: TestClient):
        """Test login with non-existent email returns 401.

        Given: Email does not exist in database
        When: POST /auth/login
        Then: Returns 401 Unauthorized
        """
        # Arrange
        payload = {
            "email": "nonexistent@example.com",
            "password": "anypassword",  # Password doesn't matter, user doesn't exist
        }

        # Act
        response = test_client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "error_code" in data
        assert data["error_code"] == "INVALID_CREDENTIALS"

    def test_login_with_invalid_password(
        self, test_client: TestClient, create_test_user
    ):
        """Test login with wrong password returns 401.

        Given: User exists but password is incorrect
        When: POST /auth/login with wrong password
        Then: Returns 401 Unauthorized
        """
        # Arrange
        pytest.helpers.run_async(
            create_test_user(email="user@example.com", full_name="User")
        )

        payload = {
            "email": "user@example.com",
            "password": "wrongpassword",
        }

        # Act
        response = test_client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_with_inactive_user(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test login with inactive user returns 403.

        Given: User exists but is_active is False
        When: POST /auth/login
        Then: Returns 403 Forbidden
        """
        # Arrange
        pytest.helpers.run_async(
            create_test_user(
                email="inactive@example.com",
                hashed_password=test_password.hashed_password,
                is_active=False,
            )
        )

        payload = {
            "email": "inactive@example.com",
            "password": "password123",
        }

        # Act
        response = test_client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_login_with_malformed_email(self, test_client: TestClient):
        """Test login with invalid email format returns 422.

        Given: Email with invalid format
        When: POST /auth/login
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "not-an-email",
            "password": "password123",
        }

        # Act
        response = test_client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_login_with_missing_password(self, test_client: TestClient):
        """Test login without password returns 422.

        Given: Payload missing password field
        When: POST /auth/login
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            # Missing password
        }

        # Act
        response = test_client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_login_tokens_are_not_empty(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test login returns non-empty JWT tokens.

        Given: Valid credentials
        When: POST /auth/login
        Then: Access token and refresh token are non-empty strings
        """
        # Arrange
        pytest.helpers.run_async(
            create_test_user(
                email="tokens@example.com",
                hashed_password=test_password.hashed_password,
            )
        )

        payload = {
            "email": "tokens@example.com",
            "password": "password123",
        }

        # Act
        response = test_client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["access_token"]) > 0
        assert len(data["refresh_token"]) > 0
        # JWT tokens should have 3 parts separated by dots
        assert data["access_token"].count(".") == 2
        assert data["refresh_token"].count(".") == 2

    def test_login_with_admin_user(
        self, test_client: TestClient, create_test_user, test_password
    ):
        """Test login with admin user returns correct role.

        Given: User with ADMIN role
        When: POST /auth/login
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

        payload = {
            "email": "admin@example.com",
            "password": "password123",
        }

        # Act
        response = test_client.post("/auth/login", json=payload)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user"]["role"] == "admin"
