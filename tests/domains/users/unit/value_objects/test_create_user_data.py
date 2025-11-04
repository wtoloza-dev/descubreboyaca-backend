"""Unit tests for CreateUserData value object.

These tests verify the CreateUserData value object validation and behavior.
"""

import pytest
from pydantic import ValidationError

from app.domains.auth.domain.enums import UserRole
from app.domains.auth.domain.value_objects import CreateUserData


class TestCreateUserData:
    """Unit tests for CreateUserData value object."""

    def test_create_user_data_with_valid_minimal_fields(self):
        """Test creating CreateUserData with minimal valid fields.

        Given: Valid email, password, and full_name
        When: CreateUserData is instantiated
        Then: Value object is created with defaults for role and is_active
        """
        # Arrange & Act
        user_data = CreateUserData(
            email="test@example.com",
            password="SecurePassword123!",
            full_name="Test User",
        )

        # Assert
        assert user_data.email == "test@example.com"
        assert user_data.password == "SecurePassword123!"
        assert user_data.full_name == "Test User"
        assert user_data.role == UserRole.USER  # Default
        assert user_data.is_active is True  # Default

    def test_create_user_data_with_all_fields(self):
        """Test creating CreateUserData with all fields specified.

        Given: All fields provided including role and is_active
        When: CreateUserData is instantiated
        Then: Value object is created with all specified values
        """
        # Arrange & Act
        user_data = CreateUserData(
            email="admin@example.com",
            password="AdminPassword123!",
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_active=False,
        )

        # Assert
        assert user_data.email == "admin@example.com"
        assert user_data.password == "AdminPassword123!"
        assert user_data.full_name == "Admin User"
        assert user_data.role == UserRole.ADMIN
        assert user_data.is_active is False

    def test_create_user_data_is_immutable(self):
        """Test that CreateUserData is immutable (frozen).

        Given: CreateUserData instance
        When: Attempting to modify a field
        Then: Raises ValidationError
        """
        # Arrange
        user_data = CreateUserData(
            email="test@example.com",
            password="Password123!",
            full_name="Test User",
        )

        # Act & Assert
        with pytest.raises(ValidationError):
            user_data.email = "newemail@example.com"

    def test_create_user_data_with_invalid_email(self):
        """Test creating CreateUserData with invalid email format.

        Given: Invalid email format
        When: CreateUserData is instantiated
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateUserData(
                email="not-an-email",
                password="Password123!",
                full_name="Test User",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("email",) for error in errors)

    def test_create_user_data_with_short_password(self):
        """Test creating CreateUserData with password less than 8 characters.

        Given: Password with less than 8 characters
        When: CreateUserData is instantiated
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateUserData(
                email="test@example.com",
                password="short",  # Only 5 characters
                full_name="Test User",
            )

        errors = exc_info.value.errors()
        assert any(
            error["loc"] == ("password",) and "at least 8 characters" in str(error)
            for error in errors
        )

    def test_create_user_data_with_long_password(self):
        """Test creating CreateUserData with password at max length.

        Given: Password at maximum length (255 characters)
        When: CreateUserData is instantiated
        Then: Value object is created successfully
        """
        # Arrange
        long_password = "A" * 255

        # Act
        user_data = CreateUserData(
            email="test@example.com",
            password=long_password,
            full_name="Test User",
        )

        # Assert
        assert len(user_data.password) == 255

    def test_create_user_data_with_password_exceeding_max_length(self):
        """Test creating CreateUserData with password exceeding max length.

        Given: Password longer than 255 characters
        When: CreateUserData is instantiated
        Then: Raises ValidationError
        """
        # Arrange
        too_long_password = "A" * 256

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateUserData(
                email="test@example.com",
                password=too_long_password,
                full_name="Test User",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("password",) for error in errors)

    def test_create_user_data_with_short_full_name(self):
        """Test creating CreateUserData with full_name less than 2 characters.

        Given: Full name with less than 2 characters
        When: CreateUserData is instantiated
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateUserData(
                email="test@example.com",
                password="Password123!",
                full_name="A",  # Only 1 character
            )

        errors = exc_info.value.errors()
        assert any(
            error["loc"] == ("full_name",) and "at least 2 characters" in str(error)
            for error in errors
        )

    def test_create_user_data_with_long_full_name(self):
        """Test creating CreateUserData with full_name at max length.

        Given: Full name at maximum length (255 characters)
        When: CreateUserData is instantiated
        Then: Value object is created successfully
        """
        # Arrange
        long_name = "A" * 255

        # Act
        user_data = CreateUserData(
            email="test@example.com",
            password="Password123!",
            full_name=long_name,
        )

        # Assert
        assert len(user_data.full_name) == 255

    def test_create_user_data_with_full_name_exceeding_max_length(self):
        """Test creating CreateUserData with full_name exceeding max length.

        Given: Full name longer than 255 characters
        When: CreateUserData is instantiated
        Then: Raises ValidationError
        """
        # Arrange
        too_long_name = "A" * 256

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateUserData(
                email="test@example.com",
                password="Password123!",
                full_name=too_long_name,
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("full_name",) for error in errors)

    def test_create_user_data_with_special_characters_in_name(self):
        """Test creating CreateUserData with special characters in full_name.

        Given: Full name with accents and special characters
        When: CreateUserData is instantiated
        Then: Value object is created with the name intact
        """
        # Arrange & Act
        user_data = CreateUserData(
            email="test@example.com",
            password="Password123!",
            full_name="José María Ñoño",
        )

        # Assert
        assert user_data.full_name == "José María Ñoño"

    def test_create_user_data_with_missing_email(self):
        """Test creating CreateUserData without email.

        Given: Missing email field
        When: CreateUserData is instantiated
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateUserData(
                password="Password123!",
                full_name="Test User",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("email",) for error in errors)

    def test_create_user_data_with_missing_password(self):
        """Test creating CreateUserData without password.

        Given: Missing password field
        When: CreateUserData is instantiated
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateUserData(
                email="test@example.com",
                full_name="Test User",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("password",) for error in errors)

    def test_create_user_data_with_missing_full_name(self):
        """Test creating CreateUserData without full_name.

        Given: Missing full_name field
        When: CreateUserData is instantiated
        Then: Raises ValidationError
        """
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CreateUserData(
                email="test@example.com",
                password="Password123!",
            )

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("full_name",) for error in errors)

    def test_create_user_data_with_owner_role(self):
        """Test creating CreateUserData with OWNER role.

        Given: Role set to OWNER
        When: CreateUserData is instantiated
        Then: Value object is created with owner role
        """
        # Arrange & Act
        user_data = CreateUserData(
            email="owner@example.com",
            password="Password123!",
            full_name="Owner User",
            role=UserRole.OWNER,
        )

        # Assert
        assert user_data.role == UserRole.OWNER

    def test_create_user_data_role_default_is_user(self):
        """Test that role defaults to USER when not specified.

        Given: CreateUserData without role specified
        When: CreateUserData is instantiated
        Then: role defaults to UserRole.USER
        """
        # Arrange & Act
        user_data = CreateUserData(
            email="test@example.com",
            password="Password123!",
            full_name="Test User",
        )

        # Assert
        assert user_data.role == UserRole.USER

    def test_create_user_data_is_active_default_is_true(self):
        """Test that is_active defaults to True when not specified.

        Given: CreateUserData without is_active specified
        When: CreateUserData is instantiated
        Then: is_active defaults to True
        """
        # Arrange & Act
        user_data = CreateUserData(
            email="test@example.com",
            password="Password123!",
            full_name="Test User",
        )

        # Assert
        assert user_data.is_active is True

    def test_create_user_data_equality(self):
        """Test that two CreateUserData with same values are equal.

        Given: Two CreateUserData instances with identical values
        When: Compared using ==
        Then: They are equal
        """
        # Arrange
        user_data_1 = CreateUserData(
            email="test@example.com",
            password="Password123!",
            full_name="Test User",
            role=UserRole.USER,
            is_active=True,
        )
        user_data_2 = CreateUserData(
            email="test@example.com",
            password="Password123!",
            full_name="Test User",
            role=UserRole.USER,
            is_active=True,
        )

        # Act & Assert
        assert user_data_1 == user_data_2

    def test_create_user_data_model_dump(self):
        """Test that CreateUserData can be dumped to dict.

        Given: CreateUserData instance
        When: model_dump() is called
        Then: Returns dict with all fields
        """
        # Arrange
        user_data = CreateUserData(
            email="test@example.com",
            password="Password123!",
            full_name="Test User",
            role=UserRole.ADMIN,
            is_active=False,
        )

        # Act
        dumped = user_data.model_dump()

        # Assert
        assert dumped["email"] == "test@example.com"
        assert dumped["password"] == "Password123!"
        assert dumped["full_name"] == "Test User"
        assert dumped["role"] == UserRole.ADMIN
        assert dumped["is_active"] is False
