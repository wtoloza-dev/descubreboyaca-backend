"""Integration tests for AuthService verification operations.

These tests verify user credential verification and token validation through service layer.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.domain.enums import AuthProvider
from app.domains.auth.domain.exceptions import (
    ExpiredTokenException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserInactiveException,
    UserNotFoundException,
)
from app.domains.auth.services import AuthService


class TestAuthServiceVerifyUserCredentials:
    """Integration tests for AuthService verify_user_credentials operation."""

    @pytest.mark.asyncio
    async def test_verify_valid_credentials_returns_user(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test verifying valid credentials returns user.

        Given: User exists with email and password
        When: Calling auth_service.verify_user_credentials()
        Then: Returns User entity
        """
        # Arrange

        user = await create_test_user(
            email="verify@example.com",
        )

        # Act
        verified_user = await auth_service.verify_user_credentials(
            "verify@example.com", "password123"
        )

        # Assert
        assert verified_user.id == user.id
        assert verified_user.email == user.email

    @pytest.mark.asyncio
    async def test_verify_nonexistent_email_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
    ):
        """Test verifying non-existent email raises InvalidCredentialsException.

        Given: Email does not exist
        When: Calling auth_service.verify_user_credentials()
        Then: Raises InvalidCredentialsException
        """
        # Arrange & Act & Assert
        with pytest.raises(InvalidCredentialsException):
            await auth_service.verify_user_credentials(
                "nonexistent@example.com", "password123"
            )

    @pytest.mark.asyncio
    async def test_verify_wrong_password_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test verifying wrong password raises InvalidCredentialsException.

        Given: User exists but password is incorrect
        When: Calling auth_service.verify_user_credentials()
        Then: Raises InvalidCredentialsException
        """
        # Arrange

        await create_test_user(
            email="wrongpass@example.com",
        )

        # Act & Assert
        with pytest.raises(InvalidCredentialsException):
            await auth_service.verify_user_credentials(
                "wrongpass@example.com", "wrongpassword"
            )

    @pytest.mark.asyncio
    async def test_verify_inactive_user_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test verifying inactive user raises UserInactiveException.

        Given: User exists but is_active is False
        When: Calling auth_service.verify_user_credentials()
        Then: Raises UserInactiveException
        """
        # Arrange

        await create_test_user(
            email="inactive@example.com",
            is_active=False,
        )

        # Act & Assert
        with pytest.raises(UserInactiveException):
            await auth_service.verify_user_credentials(
                "inactive@example.com", "password123"
            )

    @pytest.mark.asyncio
    async def test_verify_oauth_user_without_password_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test verifying OAuth user without password raises exception.

        Given: User has no password (OAuth user)
        When: Calling auth_service.verify_user_credentials()
        Then: Raises InvalidCredentialsException with OAuth message
        """
        # Arrange
        await create_test_user(
            email="oauth@example.com",
            hashed_password=None,  # OAuth users don't have passwords
            auth_provider=AuthProvider.GOOGLE,
        )

        # Act & Assert
        with pytest.raises(InvalidCredentialsException) as exc_info:
            await auth_service.verify_user_credentials("oauth@example.com", "password")

        assert "OAuth" in str(exc_info.value)


class TestAuthServiceGetCurrentUser:
    """Integration tests for AuthService get_current_user operation."""

    @pytest.mark.asyncio
    async def test_get_current_user_with_valid_token_returns_user(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test getting current user with valid token returns user.

        Given: Valid access token for existing user
        When: Calling auth_service.get_current_user()
        Then: Returns User entity
        """
        # Arrange

        user = await create_test_user(
            email="current@example.com",
        )

        # Login to get token
        tokens, _ = await auth_service.login("current@example.com", "password123")

        # Act
        current_user = await auth_service.get_current_user(tokens.access_token)

        # Assert
        assert current_user.id == user.id
        assert current_user.email == user.email

    @pytest.mark.asyncio
    async def test_get_current_user_with_invalid_token_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
    ):
        """Test get current user with invalid token raises InvalidTokenException.

        Given: Invalid or malformed token
        When: Calling auth_service.get_current_user()
        Then: Raises InvalidTokenException
        """
        # Arrange
        invalid_token = "invalid.token.here"

        # Act & Assert
        with pytest.raises(InvalidTokenException):
            await auth_service.get_current_user(invalid_token)

    @pytest.mark.asyncio
    async def test_get_current_user_with_expired_token_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
        token_provider,
    ):
        """Test get current user with expired token raises ExpiredTokenException.

        Given: Token has expired
        When: Calling auth_service.get_current_user()
        Then: Raises ExpiredTokenException
        """
        # Arrange
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        user = await create_test_user(email="expired@example.com")

        # Create expired access token
        expired_payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,  # StrEnum serializes directly
            "type": "access",
            "exp": datetime.now(UTC) - timedelta(hours=1),  # Expired
            "iat": datetime.now(UTC) - timedelta(hours=2),
        }
        expired_token = jwt.encode(
            expired_payload,
            token_provider.secret_key,
            algorithm=token_provider.algorithm,
        )

        # Act & Assert
        with pytest.raises(ExpiredTokenException):
            await auth_service.get_current_user(expired_token)

    @pytest.mark.asyncio
    async def test_get_current_user_with_deleted_user_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        token_provider,
    ):
        """Test get current user with deleted user raises UserNotFoundException.

        Given: Token for user that no longer exists
        When: Calling auth_service.get_current_user()
        Then: Raises UserNotFoundException
        """
        # Arrange
        from app.domains.auth.domain.enums import UserRole
        from app.shared.domain.factories import generate_ulid

        nonexistent_user_id = generate_ulid()

        # Create token for non-existent user
        access_token = token_provider.create_access_token(
            user_id=nonexistent_user_id,
            email="deleted@example.com",
            role=UserRole.USER,
        )

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            await auth_service.get_current_user(access_token)

    @pytest.mark.asyncio
    async def test_get_current_user_with_inactive_user_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
        user_repository,
        token_provider,
    ):
        """Test get current user with inactive user raises UserInactiveException.

        Given: User was active but is now deactivated
        When: Calling auth_service.get_current_user()
        Then: Raises UserInactiveException
        """
        # Arrange

        user = await create_test_user(
            email="deactivated@example.com",
            is_active=True,
        )

        # Login to get token
        tokens, _ = await auth_service.login("deactivated@example.com", "password123")

        # Deactivate user after login
        await user_repository.deactivate(user.id)

        # Act & Assert
        with pytest.raises(UserInactiveException):
            await auth_service.get_current_user(tokens.access_token)

    @pytest.mark.asyncio
    async def test_get_current_user_with_token_missing_sub_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        token_provider,
    ):
        """Test get current user with token missing 'sub' raises InvalidTokenException.

        Given: Token without user ID (sub claim)
        When: Calling auth_service.get_current_user()
        Then: Raises InvalidTokenException
        """
        # Arrange
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        # Create token without 'sub' claim
        invalid_payload = {
            "email": "test@example.com",
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(hours=1),
            "iat": datetime.now(UTC),
            # Missing 'sub'
        }
        invalid_token = jwt.encode(
            invalid_payload,
            token_provider.secret_key,
            algorithm=token_provider.algorithm,
        )

        # Act & Assert
        with pytest.raises(InvalidTokenException) as exc_info:
            await auth_service.get_current_user(invalid_token)

        assert "payload" in str(exc_info.value).lower()
