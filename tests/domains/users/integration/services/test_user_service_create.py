"""Integration tests for UserService.create method.

These tests verify the user creation logic through the service layer.
"""

import pytest

from app.domains.users.application.services import UserService
from app.domains.users.domain.enums import UserRole
from app.domains.users.domain.exceptions import UserAlreadyExistsException
from app.domains.users.domain.value_objects import CreateUserData


class TestUserServiceCreate:
    """Integration tests for UserService.create method."""

    @pytest.mark.asyncio
    async def test_create_user_with_valid_data(self, user_service: UserService):
        """Test creating user with valid data returns user entity.

        Given: Valid CreateUserData value object
        When: service.create() is called
        Then: Returns User entity with correct data and hashed password
        """
        # Arrange
        user_data = CreateUserData(
            email="newuser@example.com",
            password="SecurePassword123!",
            full_name="New User",
            role=UserRole.USER,
            is_active=True,
        )
        created_by = "admin_ulid_123"

        # Act
        user = await user_service.create(user_data=user_data, created_by=created_by)

        # Assert
        assert user.email == "newuser@example.com"
        assert user.full_name == "New User"
        assert user.role == UserRole.USER
        assert user.is_active is True
        assert user.hashed_password is not None
        assert user.hashed_password != "SecurePassword123!"  # Password should be hashed
        assert user.id is not None
        assert user.created_at is not None
        assert user.created_by == created_by

    @pytest.mark.asyncio
    async def test_create_admin_user(self, user_service: UserService):
        """Test creating user with admin role.

        Given: CreateUserData with role=ADMIN
        When: service.create() is called
        Then: Returns User entity with admin role
        """
        # Arrange
        user_data = CreateUserData(
            email="admin@example.com",
            password="AdminPassword123!",
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_active=True,
        )
        created_by = "super_admin_ulid"

        # Act
        user = await user_service.create(user_data=user_data, created_by=created_by)

        # Assert
        assert user.role == UserRole.ADMIN
        assert user.email == "admin@example.com"

    @pytest.mark.asyncio
    async def test_create_owner_user(self, user_service: UserService):
        """Test creating user with owner role.

        Given: CreateUserData with role=OWNER
        When: service.create() is called
        Then: Returns User entity with owner role
        """
        # Arrange
        user_data = CreateUserData(
            email="owner@example.com",
            password="OwnerPassword123!",
            full_name="Owner User",
            role=UserRole.OWNER,
            is_active=True,
        )
        created_by = "admin_ulid"

        # Act
        user = await user_service.create(user_data=user_data, created_by=created_by)

        # Assert
        assert user.role == UserRole.OWNER
        assert user.email == "owner@example.com"

    @pytest.mark.asyncio
    async def test_create_inactive_user(self, user_service: UserService):
        """Test creating inactive user.

        Given: CreateUserData with is_active=False
        When: service.create() is called
        Then: Returns inactive User entity
        """
        # Arrange
        user_data = CreateUserData(
            email="inactive@example.com",
            password="Password123!",
            full_name="Inactive User",
            role=UserRole.USER,
            is_active=False,
        )
        created_by = "admin_ulid"

        # Act
        user = await user_service.create(user_data=user_data, created_by=created_by)

        # Assert
        assert user.is_active is False
        assert user.email == "inactive@example.com"

    @pytest.mark.asyncio
    async def test_create_user_with_duplicate_email_raises_exception(
        self, user_service: UserService, create_test_user
    ):
        """Test creating user with duplicate email raises UserAlreadyExistsException.

        Given: User with email already exists
        When: service.create() is called with same email
        Then: Raises UserAlreadyExistsException
        """
        # Arrange
        await create_test_user(email="existing@example.com")
        user_data = CreateUserData(
            email="existing@example.com",
            password="Password123!",
            full_name="Duplicate User",
            role=UserRole.USER,
            is_active=True,
        )
        created_by = "admin_ulid"

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException) as exc_info:
            await user_service.create(user_data=user_data, created_by=created_by)

        assert "existing@example.com" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_user_password_is_hashed(self, user_service: UserService):
        """Test that password is properly hashed during user creation.

        Given: CreateUserData with plain text password
        When: service.create() is called
        Then: User entity has bcrypt-hashed password (starts with $2b$)
        """
        # Arrange
        plain_password = "MySecurePassword123!"
        user_data = CreateUserData(
            email="hashtest@example.com",
            password=plain_password,
            full_name="Hash Test User",
            role=UserRole.USER,
            is_active=True,
        )
        created_by = "admin_ulid"

        # Act
        user = await user_service.create(user_data=user_data, created_by=created_by)

        # Assert
        assert user.hashed_password != plain_password
        assert user.hashed_password.startswith("$2b$")  # Bcrypt hash prefix
        assert len(user.hashed_password) == 60  # Bcrypt hash length

    @pytest.mark.asyncio
    async def test_create_user_generates_ulid(self, user_service: UserService):
        """Test that user creation generates a valid ULID.

        Given: CreateUserData
        When: service.create() is called
        Then: User entity has a valid ULID (26 characters)
        """
        # Arrange
        user_data = CreateUserData(
            email="ulidtest@example.com",
            password="Password123!",
            full_name="ULID Test User",
            role=UserRole.USER,
            is_active=True,
        )
        created_by = "admin_ulid"

        # Act
        user = await user_service.create(user_data=user_data, created_by=created_by)

        # Assert
        assert user.id is not None
        assert len(user.id) == 26  # ULID length
        assert user.id.isupper()  # ULIDs are uppercase

    @pytest.mark.asyncio
    async def test_create_multiple_users_have_unique_ids(
        self, user_service: UserService
    ):
        """Test that multiple created users have unique IDs.

        Given: Multiple CreateUserData objects
        When: service.create() is called multiple times
        Then: Each user has a unique ULID
        """
        # Arrange
        user_data_1 = CreateUserData(
            email="user1@example.com",
            password="Password123!",
            full_name="User One",
            role=UserRole.USER,
            is_active=True,
        )
        user_data_2 = CreateUserData(
            email="user2@example.com",
            password="Password123!",
            full_name="User Two",
            role=UserRole.USER,
            is_active=True,
        )
        created_by = "admin_ulid"

        # Act
        user1 = await user_service.create(user_data=user_data_1, created_by=created_by)
        user2 = await user_service.create(user_data=user_data_2, created_by=created_by)

        # Assert
        assert user1.id != user2.id

    @pytest.mark.asyncio
    async def test_create_user_sets_auth_provider_to_email(
        self, user_service: UserService
    ):
        """Test that created user has auth_provider set to EMAIL.

        Given: CreateUserData
        When: service.create() is called
        Then: User entity has auth_provider='email'
        """
        # Arrange
        user_data = CreateUserData(
            email="authprovider@example.com",
            password="Password123!",
            full_name="Auth Provider Test",
            role=UserRole.USER,
            is_active=True,
        )
        created_by = "admin_ulid"

        # Act
        user = await user_service.create(user_data=user_data, created_by=created_by)

        # Assert
        assert user.auth_provider.value == "email"

    @pytest.mark.asyncio
    async def test_create_user_persists_to_database(
        self, user_service: UserService, user_repository
    ):
        """Test that created user is persisted to database.

        Given: CreateUserData
        When: service.create() is called
        Then: User can be retrieved from repository
        """
        # Arrange
        user_data = CreateUserData(
            email="persist@example.com",
            password="Password123!",
            full_name="Persist Test",
            role=UserRole.USER,
            is_active=True,
        )
        created_by = "admin_ulid"

        # Act
        created_user = await user_service.create(
            user_data=user_data, created_by=created_by
        )

        # Assert - Retrieve from repository
        retrieved_user = await user_repository.get_by_email("persist@example.com")
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == created_user.email
