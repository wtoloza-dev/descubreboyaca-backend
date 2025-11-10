"""Integration tests for AuthService login operations.

These tests verify user authentication logic through the service layer with database.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.application.services import AuthService
from app.domains.auth.domain.exceptions import InvalidCredentialsException
from app.domains.users.domain.enums import AuthProvider, UserRole
from app.domains.users.domain.exceptions import UserInactiveException


class TestAuthServiceLogin:
    """Integration tests for AuthService login operation."""

    @pytest.mark.asyncio
    async def test_login_with_valid_credentials_returns_tokens_and_user(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test login with valid credentials returns tokens and user.

        Given: User exists with email and password
        When: Calling auth_service.login() with correct credentials
        Then: Returns tuple of (tokens, user)
        """
        # Arrange

        user = await create_test_user(
            email="testuser@example.com",
            full_name="Test User",
        )

        # Act
        tokens, authenticated_user = await auth_service.login(
            "testuser@example.com", "password123"
        )

        # Assert
        assert tokens.access_token is not None
        assert tokens.refresh_token is not None
        assert tokens.token_type == "bearer"
        assert authenticated_user.id == user.id
        assert authenticated_user.email == user.email

    @pytest.mark.asyncio
    async def test_login_with_nonexistent_email_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
    ):
        """Test login with non-existent email raises InvalidCredentialsException.

        Given: Email does not exist in database
        When: Calling auth_service.login()
        Then: Raises InvalidCredentialsException
        """
        # Arrange & Act & Assert
        with pytest.raises(InvalidCredentialsException):
            await auth_service.login("nonexistent@example.com", "password123")

    @pytest.mark.asyncio
    async def test_login_with_wrong_password_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test login with wrong password raises InvalidCredentialsException.

        Given: User exists but password is incorrect
        When: Calling auth_service.login() with wrong password
        Then: Raises InvalidCredentialsException
        """
        # Arrange

        await create_test_user(
            email="user@example.com",
        )

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            await auth_service.login("user@example.com", "wrongpassword")

    @pytest.mark.asyncio
    async def test_login_with_inactive_user_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test login with inactive user raises UserInactiveException.

        Given: User exists but is_active is False
        When: Calling auth_service.login()
        Then: Raises UserInactiveException
        """
        # Arrange

        await create_test_user(
            email="inactive@example.com",
            is_active=False,
        )

        # Act & Assert
        with pytest.raises(UserInactiveException) as exc_info:
            await auth_service.login("inactive@example.com", "password123")

        assert "inactive@example.com" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_login_tokens_are_valid_jwt(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
        token_provider,
    ):
        """Test login returns valid JWT tokens.

        Given: Valid credentials
        When: Calling auth_service.login()
        Then: Returns tokens that can be verified
        """
        # Arrange

        user = await create_test_user(
            email="jwt@example.com",
        )

        # Act
        tokens, _ = await auth_service.login("jwt@example.com", "password123")

        # Assert - verify tokens
        access_payload = token_provider.verify_token(tokens.access_token)
        refresh_payload = token_provider.verify_token(tokens.refresh_token)

        assert access_payload["sub"] == user.id
        assert access_payload["email"] == user.email
        assert access_payload["type"] == "access"

        assert refresh_payload["sub"] == user.id
        assert refresh_payload["type"] == "refresh"

    @pytest.mark.asyncio
    async def test_login_with_oauth_user_without_password_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test login fails for OAuth user without password.

        Given: User registered via OAuth (no password)
        When: Calling auth_service.login() with password
        Then: Raises InvalidCredentialsException
        """
        # Arrange - OAuth user has no password
        await create_test_user(
            email="oauth@example.com",
            hashed_password=None,  # OAuth users don't have passwords
            auth_provider=AuthProvider.GOOGLE,
        )

        # Act & Assert
        with pytest.raises(InvalidCredentialsException) as exc_info:
            await auth_service.login("oauth@example.com", "password123")

        assert "OAuth" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_login_with_admin_user(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
        token_provider,
    ):
        """Test login with admin user includes role in token.

        Given: User with ADMIN role
        When: Calling auth_service.login()
        Then: Access token includes role="admin"
        """
        # Arrange

        await create_test_user(
            email="admin@example.com",
            role=UserRole.ADMIN,
        )

        # Act
        tokens, authenticated_user = await auth_service.login(
            "admin@example.com", "password123"
        )

        # Assert
        access_payload = token_provider.verify_token(tokens.access_token)
        assert access_payload["role"] == "admin"
        assert authenticated_user.role == UserRole.ADMIN

    @pytest.mark.asyncio
    async def test_login_case_sensitive_email(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test login is case-sensitive for email.

        Given: User registered with lowercase email
        When: Calling auth_service.login() with different case
        Then: Raises InvalidCredentialsException (email not found)
        """
        # Arrange

        await create_test_user(
            email="lowercase@example.com",
        )

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            await auth_service.login(
                "LOWERCASE@EXAMPLE.COM", "password123"
            )  # Different case
