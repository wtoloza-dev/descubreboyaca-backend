"""Integration tests for AuthService register operations.

These tests verify user registration logic through the service layer with database.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.domain.enums import AuthProvider, UserRole
from app.domains.auth.domain.exceptions import UserAlreadyExistsException
from app.domains.auth.services import AuthService


class TestAuthServiceRegister:
    """Integration tests for AuthService register operation."""

    @pytest.mark.asyncio
    async def test_register_creates_user_with_hashed_password(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        password_service,
    ):
        """Test registering a new user creates user with hashed password.

        Given: Valid email, password, and full_name
        When: Calling auth_service.register()
        Then: Creates user with hashed password in database
        """
        # Arrange
        email = "newuser@example.com"
        password = "SecurePassword123!"
        full_name = "New User"

        # Act
        user = await auth_service.register(email, password, full_name)

        # Assert
        assert user.email == email
        assert user.full_name == full_name
        assert user.hashed_password is not None
        assert user.hashed_password != password  # Should be hashed
        assert user.role == UserRole.USER  # Default role
        assert user.is_active is True
        assert user.auth_provider == AuthProvider.EMAIL
        assert user.id is not None  # ULID generated
        assert user.created_at is not None

    @pytest.mark.asyncio
    async def test_register_password_can_be_verified(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        password_service,
    ):
        """Test registered user's password can be verified.

        Given: User registered with password
        When: Verifying the same password
        Then: Password verification succeeds
        """
        # Arrange
        email = "verify@example.com"
        password = "SecurePassword123!"
        full_name = "Verify User"

        # Act
        user = await auth_service.register(email, password, full_name)

        # Assert - verify password
        from app.domains.auth.domain import PasswordHash

        password_hash = PasswordHash(value=user.hashed_password)
        assert password_service.verify_password(password, password_hash) is True
        assert password_service.verify_password("wrongpassword", password_hash) is False

    @pytest.mark.asyncio
    async def test_register_with_duplicate_email_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test registering with existing email raises UserAlreadyExistsException.

        Given: Email already exists in database
        When: Calling auth_service.register() with same email
        Then: Raises UserAlreadyExistsException
        """
        # Arrange
        existing_user = await create_test_user(email="existing@example.com")

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException) as exc_info:
            await auth_service.register(
                "existing@example.com",
                "password123",
                "Another User",
            )

        assert "existing@example.com" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_register_with_custom_role(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
    ):
        """Test registering user with custom role.

        Given: Role specified as ADMIN
        When: Calling auth_service.register() with role parameter
        Then: Creates user with ADMIN role
        """
        # Arrange
        email = "admin@example.com"
        password = "SecurePassword123!"
        full_name = "Admin User"

        # Act
        user = await auth_service.register(
            email, password, full_name, role=UserRole.ADMIN
        )

        # Assert
        assert user.role == UserRole.ADMIN

    @pytest.mark.asyncio
    async def test_register_with_owner_role(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
    ):
        """Test registering user with OWNER role.

        Given: Role specified as OWNER
        When: Calling auth_service.register() with role parameter
        Then: Creates user with OWNER role
        """
        # Arrange
        email = "owner@example.com"
        password = "SecurePassword123!"
        full_name = "Owner User"

        # Act
        user = await auth_service.register(
            email, password, full_name, role=UserRole.OWNER
        )

        # Assert
        assert user.role == UserRole.OWNER

    @pytest.mark.asyncio
    async def test_register_sets_default_values(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
    ):
        """Test register sets appropriate default values.

        Given: Minimal registration data
        When: Calling auth_service.register()
        Then: Sets is_active=True, auth_provider=EMAIL, role=USER
        """
        # Arrange
        email = "defaults@example.com"
        password = "SecurePassword123!"
        full_name = "Defaults User"

        # Act
        user = await auth_service.register(email, password, full_name)

        # Assert
        assert user.is_active is True
        assert user.auth_provider == AuthProvider.EMAIL
        assert user.role == UserRole.USER
        assert user.google_id is None  # OAuth fields should be None

    @pytest.mark.asyncio
    async def test_register_persists_user_to_database(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        user_repository,
    ):
        """Test register persists user to database.

        Given: Valid registration data
        When: Calling auth_service.register()
        Then: User can be retrieved from database by email
        """
        # Arrange
        email = "persisted@example.com"
        password = "SecurePassword123!"
        full_name = "Persisted User"

        # Act
        user = await auth_service.register(email, password, full_name)

        # Assert - retrieve from database
        retrieved_user = await user_repository.get_by_email(email)
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.email == email
        assert retrieved_user.full_name == full_name
