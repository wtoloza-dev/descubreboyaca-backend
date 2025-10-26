"""Integration tests for JWTTokenProvider.

These tests verify JWT token creation and verification.
"""

import pytest

from app.domains.auth.domain.enums import UserRole
from app.domains.auth.domain.exceptions import (
    ExpiredTokenException,
    InvalidTokenException,
)
from app.domains.auth.services.token import JWTTokenProvider


class TestJWTTokenProviderCreateTokens:
    """Integration tests for JWTTokenProvider token creation."""

    def test_create_access_token_returns_valid_jwt(
        self, token_provider: JWTTokenProvider
    ):
        """Test creating access token returns valid JWT.

        Given: User ID, email, and role
        When: Calling token_provider.create_access_token()
        Then: Returns JWT string with 3 parts
        """
        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"
        email = "user@example.com"
        role = UserRole.USER

        # Act
        token = token_provider.create_access_token(user_id, email, role)

        # Assert
        assert isinstance(token, str)
        assert len(token) > 0
        assert token.count(".") == 2  # JWT has 3 parts: header.payload.signature

    def test_create_refresh_token_returns_valid_jwt(
        self, token_provider: JWTTokenProvider
    ):
        """Test creating refresh token returns valid JWT.

        Given: User ID
        When: Calling token_provider.create_refresh_token()
        Then: Returns JWT string with 3 parts
        """
        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"

        # Act
        token = token_provider.create_refresh_token(user_id)

        # Assert
        assert isinstance(token, str)
        assert len(token) > 0
        assert token.count(".") == 2

    def test_access_token_contains_expected_claims(
        self, token_provider: JWTTokenProvider
    ):
        """Test access token contains expected claims.

        Given: User data
        When: Creating access token
        Then: Token payload includes sub, email, role, type, exp, iat
        """
        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"
        email = "user@example.com"
        role = UserRole.ADMIN

        # Act
        token = token_provider.create_access_token(user_id, email, role)
        payload = token_provider.verify_token(token)

        # Assert
        assert payload["sub"] == user_id
        assert payload["email"] == email
        assert payload["role"] == "admin"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload

    def test_refresh_token_contains_expected_claims(
        self, token_provider: JWTTokenProvider
    ):
        """Test refresh token contains expected claims.

        Given: User ID
        When: Creating refresh token
        Then: Token payload includes sub, type, exp, iat (minimal claims)
        """
        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"

        # Act
        token = token_provider.create_refresh_token(user_id)
        payload = token_provider.verify_token(token)

        # Assert
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
        assert "email" not in payload  # Refresh tokens have minimal claims
        assert "role" not in payload

    def test_access_token_and_refresh_token_are_different(
        self, token_provider: JWTTokenProvider
    ):
        """Test access and refresh tokens are different for same user.

        Given: Same user ID
        When: Creating access and refresh tokens
        Then: Tokens are different
        """
        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"

        # Act
        access_token = token_provider.create_access_token(
            user_id, "user@example.com", UserRole.USER
        )
        refresh_token = token_provider.create_refresh_token(user_id)

        # Assert
        assert access_token != refresh_token

    def test_create_multiple_tokens_for_same_user_are_different(
        self, token_provider: JWTTokenProvider
    ):
        """Test multiple tokens for same user are different due to timestamps.

        Given: Same user ID
        When: Creating multiple access tokens
        Then: Tokens are different (different iat timestamps)
        """
        import time

        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"
        email = "user@example.com"
        role = UserRole.USER

        # Act
        token1 = token_provider.create_access_token(user_id, email, role)
        time.sleep(
            1
        )  # JWT timestamps are in seconds, need at least 1 second difference
        token2 = token_provider.create_access_token(user_id, email, role)

        # Assert
        # Tokens will be different due to different iat (issued at) timestamps
        assert token1 != token2


class TestJWTTokenProviderVerifyToken:
    """Integration tests for JWTTokenProvider token verification."""

    def test_verify_valid_access_token(self, token_provider: JWTTokenProvider):
        """Test verifying valid access token returns payload.

        Given: Valid access token
        When: Calling token_provider.verify_token()
        Then: Returns decoded payload dictionary
        """
        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"
        token = token_provider.create_access_token(
            user_id, "user@example.com", UserRole.USER
        )

        # Act
        payload = token_provider.verify_token(token)

        # Assert
        assert isinstance(payload, dict)
        assert payload["sub"] == user_id

    def test_verify_valid_refresh_token(self, token_provider: JWTTokenProvider):
        """Test verifying valid refresh token returns payload.

        Given: Valid refresh token
        When: Calling token_provider.verify_token()
        Then: Returns decoded payload dictionary
        """
        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"
        token = token_provider.create_refresh_token(user_id)

        # Act
        payload = token_provider.verify_token(token)

        # Assert
        assert isinstance(payload, dict)
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"

    def test_verify_invalid_token_raises_exception(
        self, token_provider: JWTTokenProvider
    ):
        """Test verifying invalid token raises InvalidTokenException.

        Given: Malformed or invalid token
        When: Calling token_provider.verify_token()
        Then: Raises InvalidTokenException
        """
        # Arrange
        invalid_token = "invalid.token.here"

        # Act & Assert
        with pytest.raises(InvalidTokenException):
            token_provider.verify_token(invalid_token)

    def test_verify_expired_token_raises_exception(
        self, token_provider: JWTTokenProvider
    ):
        """Test verifying expired token raises ExpiredTokenException.

        Given: Token that has expired
        When: Calling token_provider.verify_token()
        Then: Raises ExpiredTokenException
        """
        # Arrange
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        # Create expired token
        expired_payload = {
            "sub": "01HQZX123456789ABCDEFGHIJK",
            "email": "user@example.com",
            "role": "user",
            "type": "access",
            "exp": datetime.now(UTC) - timedelta(hours=1),  # Expired 1 hour ago
            "iat": datetime.now(UTC) - timedelta(hours=2),
        }
        expired_token = jwt.encode(
            expired_payload,
            token_provider.secret_key,
            algorithm=token_provider.algorithm,
        )

        # Act & Assert
        with pytest.raises(ExpiredTokenException):
            token_provider.verify_token(expired_token)

    def test_verify_token_with_wrong_secret_raises_exception(
        self, token_provider: JWTTokenProvider
    ):
        """Test verifying token with wrong secret raises InvalidTokenException.

        Given: Token signed with different secret
        When: Calling token_provider.verify_token()
        Then: Raises InvalidTokenException
        """
        # Arrange
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        # Create token with different secret
        payload = {
            "sub": "01HQZX123456789ABCDEFGHIJK",
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(hours=1),
            "iat": datetime.now(UTC),
        }
        wrong_token = jwt.encode(payload, "wrong-secret-key", algorithm="HS256")

        # Act & Assert
        with pytest.raises(InvalidTokenException):
            token_provider.verify_token(wrong_token)

    def test_verify_token_with_tampered_payload_raises_exception(
        self, token_provider: JWTTokenProvider
    ):
        """Test verifying token with tampered payload raises InvalidTokenException.

        Given: Token with modified payload
        When: Calling token_provider.verify_token()
        Then: Raises InvalidTokenException
        """
        # Arrange
        token = token_provider.create_access_token(
            "01HQZX123456789ABCDEFGHIJK", "user@example.com", UserRole.USER
        )

        # Tamper with token by modifying middle part
        parts = token.split(".")
        tampered_token = f"{parts[0]}.{parts[1][::-1]}.{parts[2]}"  # Reverse payload

        # Act & Assert
        with pytest.raises(InvalidTokenException):
            token_provider.verify_token(tampered_token)


class TestJWTTokenProviderDecodeToken:
    """Integration tests for JWTTokenProvider decode_token (without verification)."""

    def test_decode_token_without_verification(self, token_provider: JWTTokenProvider):
        """Test decoding token without verification.

        Given: Valid token
        When: Calling token_provider.decode_token()
        Then: Returns payload without verifying signature or expiration
        """
        # Arrange
        user_id = "01HQZX123456789ABCDEFGHIJK"
        token = token_provider.create_access_token(
            user_id, "user@example.com", UserRole.USER
        )

        # Act
        payload = token_provider.decode_token(token)

        # Assert
        assert isinstance(payload, dict)
        assert payload["sub"] == user_id

    def test_decode_expired_token_succeeds(self, token_provider: JWTTokenProvider):
        """Test decoding expired token without verification succeeds.

        Given: Expired token
        When: Calling token_provider.decode_token()
        Then: Returns payload (doesn't check expiration)
        """
        # Arrange
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        # Create expired token
        expired_payload = {
            "sub": "01HQZX123456789ABCDEFGHIJK",
            "type": "access",
            "exp": datetime.now(UTC) - timedelta(hours=1),  # Expired
            "iat": datetime.now(UTC) - timedelta(hours=2),
        }
        expired_token = jwt.encode(
            expired_payload,
            token_provider.secret_key,
            algorithm=token_provider.algorithm,
        )

        # Act
        payload = token_provider.decode_token(expired_token)

        # Assert
        assert isinstance(payload, dict)
        assert payload["sub"] == "01HQZX123456789ABCDEFGHIJK"


class TestJWTTokenProviderConfiguration:
    """Integration tests for JWTTokenProvider configuration."""

    def test_custom_access_token_expiration(self):
        """Test creating provider with custom access token expiration.

        Given: Custom access_token_expire_minutes
        When: Creating tokens
        Then: Token expiration reflects configuration
        """
        # Arrange
        custom_provider = JWTTokenProvider(
            secret_key="test-secret",
            access_token_expire_minutes=60,  # 1 hour
        )

        # Act
        token = custom_provider.create_access_token(
            "01HQZX123456789ABCDEFGHIJK", "user@example.com", UserRole.USER
        )
        payload = custom_provider.verify_token(token)

        # Assert
        from datetime import UTC, datetime

        exp_time = datetime.fromtimestamp(payload["exp"], UTC)
        iat_time = datetime.fromtimestamp(payload["iat"], UTC)
        duration = exp_time - iat_time

        # Should be approximately 60 minutes
        assert 59 <= duration.total_seconds() / 60 <= 61

    def test_custom_refresh_token_expiration(self):
        """Test creating provider with custom refresh token expiration.

        Given: Custom refresh_token_expire_days
        When: Creating tokens
        Then: Token expiration reflects configuration
        """
        # Arrange
        custom_provider = JWTTokenProvider(
            secret_key="test-secret",
            refresh_token_expire_days=30,  # 30 days
        )

        # Act
        token = custom_provider.create_refresh_token("01HQZX123456789ABCDEFGHIJK")
        payload = custom_provider.verify_token(token)

        # Assert
        from datetime import UTC, datetime

        exp_time = datetime.fromtimestamp(payload["exp"], UTC)
        iat_time = datetime.fromtimestamp(payload["iat"], UTC)
        duration = exp_time - iat_time

        # Should be approximately 30 days
        assert 29 <= duration.days <= 31
