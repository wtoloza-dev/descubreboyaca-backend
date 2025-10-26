"""E2E tests for POST /auth/register endpoint.

These tests verify user registration through the HTTP API.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestRegisterUser:
    """E2E tests for user registration endpoint."""

    def test_register_with_valid_data(self, test_client: TestClient):
        """Test user registration with valid data returns 201.

        Given: Valid registration data (email, password, full_name)
        When: POST /auth/register
        Then: Returns 201 with user data and success message
        """
        # Arrange
        payload = {
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
            "full_name": "New User",
        }

        # Act
        response = test_client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["message"] == "User registered successfully"
        assert "user" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["full_name"] == "New User"
        assert data["user"]["role"] == "user"
        assert data["user"]["is_active"] is True
        assert "id" in data["user"]
        assert "created_at" in data["user"]
        assert "hashed_password" not in data["user"]  # Should not expose password

    def test_register_with_duplicate_email(
        self, test_client: TestClient, create_test_user
    ):
        """Test registration with existing email returns 409.

        Given: Email already exists in database
        When: POST /auth/register with same email
        Then: Returns 409 Conflict
        """
        # Arrange
        existing_user = pytest.helpers.run_async(
            create_test_user(email="existing@example.com")
        )
        payload = {
            "email": "existing@example.com",
            "password": "SecurePassword123!",
            "full_name": "Another User",
        }

        # Act
        response = test_client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert "error_code" in data
        assert data["error_code"] == "USER_ALREADY_EXISTS"

    def test_register_with_invalid_email_format(self, test_client: TestClient):
        """Test registration with invalid email format returns 422.

        Given: Invalid email format
        When: POST /auth/register
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "not-an-email",
            "password": "SecurePassword123!",
            "full_name": "Test User",
        }

        # Act
        response = test_client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_register_with_short_password(self, test_client: TestClient):
        """Test registration with password less than 8 characters returns 422.

        Given: Password with less than 8 characters
        When: POST /auth/register
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "short",  # Only 5 characters
            "full_name": "Test User",
        }

        # Act
        response = test_client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        data = response.json()
        assert "detail" in data

    def test_register_with_short_full_name(self, test_client: TestClient):
        """Test registration with full_name less than 2 characters returns 422.

        Given: Full name with less than 2 characters
        When: POST /auth/register
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "SecurePassword123!",
            "full_name": "A",  # Only 1 character
        }

        # Act
        response = test_client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_register_with_missing_fields(self, test_client: TestClient):
        """Test registration with missing required fields returns 422.

        Given: Payload missing required fields
        When: POST /auth/register
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            # Missing password and full_name
        }

        # Act
        response = test_client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_register_includes_all_expected_fields(self, test_client: TestClient):
        """Test registration response includes all expected user fields.

        Given: Valid registration data
        When: POST /auth/register
        Then: Response includes id, email, full_name, role, is_active, created_at
        """
        # Arrange
        payload = {
            "email": "complete@example.com",
            "password": "SecurePassword123!",
            "full_name": "Complete User",
        }

        # Act
        response = test_client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        user = data["user"]
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
            assert field in user, f"Expected field '{field}' not found in response"

    def test_register_with_special_characters_in_name(self, test_client: TestClient):
        """Test registration with special characters in full name.

        Given: Full name with accents and special characters
        When: POST /auth/register
        Then: Returns 201 and accepts the name
        """
        # Arrange
        payload = {
            "email": "special@example.com",
            "password": "SecurePassword123!",
            "full_name": "José María Ñoño",
        }

        # Act
        response = test_client.post("/auth/register", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user"]["full_name"] == "José María Ñoño"
