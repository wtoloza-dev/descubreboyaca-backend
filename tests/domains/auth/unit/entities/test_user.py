"""Unit tests for User and UserData entities.

These tests verify domain validation rules and entity behavior.
"""

import pytest
from pydantic import ValidationError

from app.domains.users.domain import User, UserData
from app.domains.users.domain.enums import AuthProvider, UserRole


class TestUserData:
    """Unit tests for UserData validation."""

    def test_create_user_data_with_valid_minimal_fields(self):
        """Test creating UserData with valid minimal required fields.

        Given: Valid email and full_name
        When: Creating UserData instance
        Then: Instance is created with default values
        """
        # Arrange & Act
        user_data = UserData(
            email="user@example.com",
            full_name="Test User",
            hashed_password="hashed_password_here",
        )

        # Assert
        assert user_data.email == "user@example.com"
        assert user_data.full_name == "Test User"
        assert user_data.hashed_password == "hashed_password_here"
        assert user_data.role == UserRole.USER  # Default
        assert user_data.is_active is True  # Default
        assert user_data.auth_provider == AuthProvider.EMAIL  # Default
        assert user_data.google_id is None  # Default
        assert user_data.profile_picture_url is None  # Default

    def test_create_user_data_with_all_fields(self):
        """Test creating UserData with all optional fields specified.

        Given: All fields provided
        When: Creating UserData instance
        Then: All fields are set correctly
        """
        # Arrange & Act
        user_data = UserData(
            email="complete@example.com",
            full_name="Complete User",
            hashed_password="hashed_password",
            role=UserRole.ADMIN,
            is_active=False,
            auth_provider=AuthProvider.GOOGLE,
            google_id="google_oauth_123",
            profile_picture_url="https://example.com/pic.jpg",
        )

        # Assert
        assert user_data.email == "complete@example.com"
        assert user_data.full_name == "Complete User"
        assert user_data.role == UserRole.ADMIN
        assert user_data.is_active is False
        assert user_data.auth_provider == AuthProvider.GOOGLE
        assert user_data.google_id == "google_oauth_123"
        assert user_data.profile_picture_url == "https://example.com/pic.jpg"

    def test_create_user_data_with_invalid_email(self):
        """Test creating UserData with invalid email raises ValidationError.

        Given: Invalid email format
        When: Creating UserData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserData(
                email="not-an-email",  # Invalid email
                full_name="Test User",
                hashed_password="password",
            )

        assert "email" in str(exc_info.value).lower()

    def test_create_user_data_with_short_full_name(self):
        """Test creating UserData with full_name less than 2 chars raises ValidationError.

        Given: full_name with 1 character
        When: Creating UserData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserData(
                email="user@example.com",
                full_name="A",  # Too short (min_length=2)
                hashed_password="password",
            )

        assert "full_name" in str(exc_info.value).lower()

    def test_create_user_data_with_long_full_name(self):
        """Test creating UserData with full_name exceeding max length raises ValidationError.

        Given: full_name with more than 255 characters
        When: Creating UserData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserData(
                email="user@example.com",
                full_name="A" * 256,  # Too long (max_length=255)
                hashed_password="password",
            )

        assert "full_name" in str(exc_info.value).lower()

    def test_create_user_data_with_special_characters_in_name(self):
        """Test creating UserData with special characters in full_name.

        Given: full_name with accents and special characters
        When: Creating UserData instance
        Then: Accepts the name
        """
        # Arrange & Act
        user_data = UserData(
            email="special@example.com",
            full_name="José María Ñoño",
            hashed_password="password",
        )

        # Assert
        assert user_data.full_name == "José María Ñoño"

    def test_create_user_data_without_password_for_oauth(self):
        """Test creating UserData without password (OAuth user).

        Given: hashed_password=None (OAuth user)
        When: Creating UserData instance
        Then: Accepts None for hashed_password
        """
        # Arrange & Act
        user_data = UserData(
            email="oauth@example.com",
            full_name="OAuth User",
            hashed_password=None,  # OAuth users don't have passwords
            auth_provider=AuthProvider.GOOGLE,
        )

        # Assert
        assert user_data.hashed_password is None
        assert user_data.auth_provider == AuthProvider.GOOGLE

    def test_create_user_data_with_long_password_hash(self):
        """Test creating UserData with password hash exceeding max length.

        Given: hashed_password longer than 255 characters
        When: Creating UserData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserData(
                email="user@example.com",
                full_name="Test User",
                hashed_password="A" * 256,  # Too long
            )

        assert "hashed_password" in str(exc_info.value).lower()

    def test_create_user_data_with_missing_email(self):
        """Test creating UserData without email raises ValidationError.

        Given: Missing email field
        When: Creating UserData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserData(
                full_name="Test User",
                hashed_password="password",
            )

        assert "email" in str(exc_info.value).lower()

    def test_create_user_data_with_missing_full_name(self):
        """Test creating UserData without full_name raises ValidationError.

        Given: Missing full_name field
        When: Creating UserData instance
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserData(
                email="user@example.com",
                hashed_password="password",
            )

        assert "full_name" in str(exc_info.value).lower()


class TestUser:
    """Unit tests for User entity."""

    def test_create_user_generates_ulid(self):
        """Test creating User automatically generates ULID.

        Given: UserData without ID
        When: Creating User instance
        Then: ID is auto-generated as ULID
        """
        # Arrange & Act
        user = User(
            email="user@example.com",
            full_name="Test User",
            hashed_password="password",
        )

        # Assert
        assert user.id is not None
        assert len(user.id) == 26  # ULID length
        assert isinstance(user.id, str)

    def test_create_user_generates_created_at(self):
        """Test creating User automatically sets created_at timestamp.

        Given: UserData without created_at
        When: Creating User instance
        Then: created_at is auto-generated
        """
        # Arrange & Act
        user = User(
            email="user@example.com",
            full_name="Test User",
            hashed_password="password",
        )

        # Assert
        assert user.created_at is not None
        from datetime import datetime

        assert isinstance(user.created_at, datetime)

    def test_create_user_with_explicit_id(self):
        """Test creating User with explicit ID.

        Given: Explicit ID provided
        When: Creating User instance
        Then: Uses provided ID instead of generating
        """
        # Arrange
        custom_id = "01HQZX123456789ABCDEFGHIJK"

        # Act
        user = User(
            id=custom_id,
            email="user@example.com",
            full_name="Test User",
            hashed_password="password",
        )

        # Assert
        assert user.id == custom_id

    def test_create_user_updated_at_defaults_to_none(self):
        """Test creating User sets updated_at to None by default.

        Given: New user
        When: Creating User instance
        Then: updated_at is None (not yet updated)
        """
        # Arrange & Act
        user = User(
            email="user@example.com",
            full_name="Test User",
            hashed_password="password",
        )

        # Assert
        assert user.updated_at is None

    def test_create_user_with_all_metadata_fields(self):
        """Test creating User with all metadata fields specified.

        Given: All fields including ID, created_at, updated_at
        When: Creating User instance
        Then: All fields are set correctly
        """
        # Arrange
        from datetime import UTC, datetime

        custom_id = "01HQZX123456789ABCDEFGHIJK"
        created_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)
        updated_at = datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC)

        # Act
        user = User(
            id=custom_id,
            email="user@example.com",
            full_name="Test User",
            hashed_password="password",
            created_at=created_at,
            updated_at=updated_at,
        )

        # Assert
        assert user.id == custom_id
        assert user.created_at == created_at
        assert user.updated_at == updated_at

    def test_user_inherits_user_data_validation(self):
        """Test User inherits validation rules from UserData.

        Given: Invalid email in User
        When: Creating User instance
        Then: Raises ValidationError (inherited validation)
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError):
            User(
                email="not-an-email",  # Invalid
                full_name="Test User",
                hashed_password="password",
            )

    def test_user_model_dump_includes_all_fields(self):
        """Test User.model_dump() includes all fields.

        Given: User instance
        When: Calling model_dump()
        Then: Returns dictionary with all fields
        """
        # Arrange
        user = User(
            email="user@example.com",
            full_name="Test User",
            hashed_password="password",
            role=UserRole.ADMIN,
        )

        # Act
        data = user.model_dump()

        # Assert
        assert "id" in data
        assert "email" in data
        assert "full_name" in data
        assert "hashed_password" in data
        assert "role" in data
        assert "is_active" in data
        assert "auth_provider" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_user_model_dump_mode_json_serializes_datetime(self):
        """Test User.model_dump(mode='json') serializes datetime to string.

        Given: User with datetime fields
        When: Calling model_dump(mode='json')
        Then: Datetime fields are serialized as ISO strings
        """
        # Arrange
        user = User(
            email="user@example.com",
            full_name="Test User",
            hashed_password="password",
        )

        # Act
        data = user.model_dump(mode="json")

        # Assert
        assert isinstance(data["created_at"], str)  # Serialized to ISO string
        assert "T" in data["created_at"]  # ISO format

    def test_user_model_dump_mode_json_serializes_enum(self):
        """Test User.model_dump(mode='json') serializes enums to values.

        Given: User with enum fields (role, auth_provider)
        When: Calling model_dump(mode='json')
        Then: Enum fields are serialized as strings
        """
        # Arrange
        user = User(
            email="user@example.com",
            full_name="Test User",
            hashed_password="password",
            role=UserRole.ADMIN,
            auth_provider=AuthProvider.GOOGLE,
        )

        # Act
        data = user.model_dump(mode="json")

        # Assert
        assert data["role"] == "admin"  # Enum value
        assert data["auth_provider"] == "google"  # Enum value
        assert isinstance(data["role"], str)
        assert isinstance(data["auth_provider"], str)

    def test_multiple_users_have_unique_ids(self):
        """Test multiple User instances get unique IDs.

        Given: Multiple users created
        When: Creating multiple User instances
        Then: Each gets a unique ULID
        """
        # Arrange & Act
        user1 = User(
            email="user1@example.com",
            full_name="User 1",
            hashed_password="password",
        )
        user2 = User(
            email="user2@example.com",
            full_name="User 2",
            hashed_password="password",
        )

        # Assert
        assert user1.id != user2.id
        assert len(user1.id) == 26
        assert len(user2.id) == 26
