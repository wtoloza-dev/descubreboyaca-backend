"""E2E tests for POST /admin/users/ endpoint.

These tests verify admin user creation through the HTTP API.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestCreateUserAdmin:
    """E2E tests for admin user creation endpoint."""

    def test_create_user_with_valid_data(self, admin_client: TestClient):
        """Test admin can create user with valid data returns 201.

        Given: Valid user creation data and admin authentication
        When: POST /admin/users/
        Then: Returns 201 with created user data
        """
        # Arrange
        payload = {
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
            "full_name": "New Test User",
            "role": "user",
            "is_active": True,
        }

        # Act
        response = admin_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New Test User"
        assert data["role"] == "user"
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data
        assert "hashed_password" not in data

    def test_create_admin_user(self, admin_client: TestClient):
        """Test admin can create another admin user.

        Given: Valid admin user creation data
        When: POST /admin/users/ with role=admin
        Then: Returns 201 with admin user data
        """
        # Arrange
        payload = {
            "email": "newadmin@example.com",
            "password": "SecurePassword123!",
            "full_name": "New Admin",
            "role": "admin",
            "is_active": True,
        }

        # Act
        response = admin_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["role"] == "admin"
        assert data["email"] == "newadmin@example.com"

    def test_create_owner_user(self, test_client: TestClient, admin_client: TestClient):
        """Test admin can create owner user.

        Given: Valid owner user creation data
        When: POST /admin/users/ with role=owner
        Then: Returns 201 with owner user data
        """
        # Arrange
        payload = {
            "email": "newowner@example.com",
            "password": "SecurePassword123!",
            "full_name": "New Owner",
            "role": "owner",
            "is_active": True,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["role"] == "owner"
        assert data["email"] == "newowner@example.com"

    def test_create_user_with_duplicate_email(
        self, test_client: TestClient, admin_client: TestClient, create_test_user
    ):
        """Test creating user with existing email returns 409.

        Given: Email already exists in database
        When: POST /admin/users/ with same email
        Then: Returns 409 Conflict
        """
        # Arrange
        pytest.helpers.run_async(create_test_user(email="existing@example.com"))
        payload = {
            "email": "existing@example.com",
            "password": "SecurePassword123!",
            "full_name": "Another User",
            "role": "user",
            "is_active": True,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert "error_code" in data
        assert data["error_code"] == "USER_ALREADY_EXISTS"

    def test_create_user_with_invalid_email_format(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test creating user with invalid email format returns 422.

        Given: Invalid email format
        When: POST /admin/users/
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "not-an-email",
            "password": "SecurePassword123!",
            "full_name": "Test User",
            "role": "user",
            "is_active": True,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_with_short_password(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test creating user with password less than 8 characters returns 422.

        Given: Password with less than 8 characters
        When: POST /admin/users/
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "short",  # Only 5 characters
            "full_name": "Test User",
            "role": "user",
            "is_active": True,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_with_short_full_name(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test creating user with full_name less than 2 characters returns 422.

        Given: Full name with less than 2 characters
        When: POST /admin/users/
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "SecurePassword123!",
            "full_name": "A",  # Only 1 character
            "role": "user",
            "is_active": True,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_with_missing_fields(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test creating user with missing required fields returns 422.

        Given: Payload missing required fields
        When: POST /admin/users/
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            # Missing password, full_name, role
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_user_with_invalid_role(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test creating user with invalid role returns 422.

        Given: Invalid role value
        When: POST /admin/users/
        Then: Returns 422 Unprocessable Entity
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "SecurePassword123!",
            "full_name": "Test User",
            "role": "invalid_role",
            "is_active": True,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_inactive_user(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test admin can create inactive user.

        Given: Valid user data with is_active=false
        When: POST /admin/users/
        Then: Returns 201 with inactive user
        """
        # Arrange
        payload = {
            "email": "inactive@example.com",
            "password": "SecurePassword123!",
            "full_name": "Inactive User",
            "role": "user",
            "is_active": False,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["is_active"] is False

    def test_create_user_without_authentication(self, test_client: TestClient):
        """Test creating user without authentication returns 401.

        Given: No authentication provided
        When: POST /admin/users/
        Then: Returns 401 Unauthorized
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "SecurePassword123!",
            "full_name": "Test User",
            "role": "user",
            "is_active": True,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_user_as_non_admin(self, owner_client: TestClient):
        """Test creating user as non-admin returns 403.

        Given: Authenticated as owner (not admin)
        When: POST /admin/users/
        Then: Returns 403 Forbidden
        """
        # Arrange
        payload = {
            "email": "user@example.com",
            "password": "SecurePassword123!",
            "full_name": "Test User",
            "role": "user",
            "is_active": True,
        }

        # Act
        response = owner_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_user_with_special_characters_in_name(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test creating user with special characters in full name.

        Given: Full name with accents and special characters
        When: POST /admin/users/
        Then: Returns 201 and accepts the name
        """
        # Arrange
        payload = {
            "email": "special@example.com",
            "password": "SecurePassword123!",
            "full_name": "José María Ñoño",
            "role": "user",
            "is_active": True,
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["full_name"] == "José María Ñoño"

    def test_create_user_default_role_is_user(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test creating user without specifying role defaults to 'user'.

        Given: User data without explicit role
        When: POST /admin/users/
        Then: Returns 201 with role='user'
        """
        # Arrange
        payload = {
            "email": "defaultrole@example.com",
            "password": "SecurePassword123!",
            "full_name": "Default Role User",
            # role omitted - should default to 'user'
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["role"] == "user"

    def test_create_user_default_is_active_is_true(
        self, test_client: TestClient, admin_client: TestClient
    ):
        """Test creating user without specifying is_active defaults to True.

        Given: User data without explicit is_active
        When: POST /admin/users/
        Then: Returns 201 with is_active=true
        """
        # Arrange
        payload = {
            "email": "defaultactive@example.com",
            "password": "SecurePassword123!",
            "full_name": "Default Active User",
            "role": "user",
            # is_active omitted - should default to True
        }

        # Act
        response = test_client.post("/api/v1/users/admin/", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["is_active"] is True
