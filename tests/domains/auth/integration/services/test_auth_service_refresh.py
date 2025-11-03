"""Integration tests for AuthService refresh token operations.

These tests verify token refresh logic through the service layer with database.
"""

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.auth.domain.exceptions import (
    ExpiredTokenException,
    InvalidTokenException,
    UserInactiveException,
    UserNotFoundException,
)
from app.domains.auth.services import AuthService


class TestAuthServiceRefreshAccessToken:
    """Integration tests for AuthService refresh access token operation."""

    @pytest.mark.asyncio
    async def test_refresh_with_valid_refresh_token_returns_new_tokens(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test refresh with valid refresh token returns new access token.

        Given: User has valid refresh token
        When: Calling auth_service.refresh_access_token()
        Then: Returns new TokenData with fresh access token
        """
        # Arrange

        await create_test_user(
            email="refresh@example.com",
        )

        # Login to get refresh token
        tokens, _ = await auth_service.login("refresh@example.com", "password123")
        original_refresh_token = tokens.refresh_token

        # Act
        new_tokens = await auth_service.refresh_access_token(original_refresh_token)

        # Assert
        assert new_tokens.access_token is not None
        assert new_tokens.refresh_token is not None
        assert new_tokens.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_refresh_with_invalid_token_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
    ):
        """Test refresh with invalid token raises InvalidTokenException.

        Given: Invalid or malformed refresh token
        When: Calling auth_service.refresh_access_token()
        Then: Raises InvalidTokenException
        """
        # Arrange
        invalid_token = "invalid.token.here"

        # Act & Assert
        with pytest.raises(InvalidTokenException):
            await auth_service.refresh_access_token(invalid_token)

    @pytest.mark.asyncio
    async def test_refresh_with_expired_token_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
        token_provider,
    ):
        """Test refresh with expired token raises ExpiredTokenException.

        Given: Refresh token has expired
        When: Calling auth_service.refresh_access_token()
        Then: Raises ExpiredTokenException
        """
        # Arrange
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        user = await create_test_user(email="expired@example.com")

        # Create expired refresh token
        expired_payload = {
            "sub": user.id,
            "type": "refresh",
            "exp": datetime.now(UTC) - timedelta(days=1),  # Expired
            "iat": datetime.now(UTC) - timedelta(days=8),
        }
        expired_token = jwt.encode(
            expired_payload,
            token_provider.secret_key,
            algorithm=token_provider.algorithm,
        )

        # Act & Assert
        with pytest.raises(ExpiredTokenException):
            await auth_service.refresh_access_token(expired_token)

    @pytest.mark.asyncio
    async def test_refresh_with_access_token_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test refresh with access token raises InvalidTokenException.

        Given: Access token instead of refresh token
        When: Calling auth_service.refresh_access_token()
        Then: Raises InvalidTokenException (wrong token type)
        """
        # Arrange

        await create_test_user(
            email="wrongtype@example.com",
        )

        # Login to get tokens
        tokens, _ = await auth_service.login("wrongtype@example.com", "password123")
        access_token = tokens.access_token  # Use access token instead

        # Act & Assert
        with pytest.raises(InvalidTokenException) as exc_info:
            await auth_service.refresh_access_token(access_token)

        assert "type" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_refresh_with_nonexistent_user_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        token_provider,
    ):
        """Test refresh with deleted user raises UserNotFoundException.

        Given: Token for user that no longer exists
        When: Calling auth_service.refresh_access_token()
        Then: Raises UserNotFoundException
        """
        # Arrange
        from app.shared.domain.factories import generate_ulid

        nonexistent_user_id = generate_ulid()

        # Create a valid refresh token for non-existent user
        refresh_token = token_provider.create_refresh_token(nonexistent_user_id)

        # Act & Assert
        with pytest.raises(UserNotFoundException):
            await auth_service.refresh_access_token(refresh_token)

    @pytest.mark.asyncio
    async def test_refresh_with_inactive_user_raises_exception(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
        user_repository,
    ):
        """Test refresh with inactive user raises UserInactiveException.

        Given: User was active but is now deactivated
        When: Calling auth_service.refresh_access_token()
        Then: Raises UserInactiveException
        """
        # Arrange

        user = await create_test_user(
            email="deactivated@example.com",
            is_active=True,
        )

        # Login to get refresh token
        tokens, _ = await auth_service.login("deactivated@example.com", "password123")
        refresh_token = tokens.refresh_token

        # Deactivate user after login
        await user_repository.deactivate(user.id)

        # Act & Assert
        with pytest.raises(UserInactiveException):
            await auth_service.refresh_access_token(refresh_token)

    @pytest.mark.asyncio
    async def test_refresh_returns_different_tokens(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
    ):
        """Test refresh returns different tokens from original.

        Given: Valid refresh token
        When: Calling auth_service.refresh_access_token()
        Then: Returns new tokens different from original
        """
        # Arrange

        await create_test_user(
            email="newtokens@example.com",
        )

        # Login to get original tokens
        original_tokens, _ = await auth_service.login(
            "newtokens@example.com", "password123"
        )

        # Wait to ensure different timestamp (JWT uses seconds)
        import asyncio

        await asyncio.sleep(1)

        # Act
        new_tokens = await auth_service.refresh_access_token(
            original_tokens.refresh_token
        )

        # Assert
        assert new_tokens.access_token != original_tokens.access_token
        # Refresh token should also be new
        assert new_tokens.refresh_token != original_tokens.refresh_token

    @pytest.mark.asyncio
    async def test_refresh_new_tokens_are_valid(
        self,
        test_session: AsyncSession,
        auth_service: AuthService,
        create_test_user,
        token_provider,
    ):
        """Test refreshed tokens can be verified.

        Given: Valid refresh token
        When: Calling auth_service.refresh_access_token()
        Then: New tokens can be successfully verified
        """
        # Arrange

        user = await create_test_user(
            email="valid@example.com",
        )

        # Login to get refresh token
        tokens, _ = await auth_service.login("valid@example.com", "password123")

        # Act
        new_tokens = await auth_service.refresh_access_token(tokens.refresh_token)

        # Assert - verify new tokens
        access_payload = token_provider.verify_token(new_tokens.access_token)
        refresh_payload = token_provider.verify_token(new_tokens.refresh_token)

        assert access_payload["sub"] == user.id
        assert access_payload["type"] == "access"
        assert refresh_payload["sub"] == user.id
        assert refresh_payload["type"] == "refresh"
