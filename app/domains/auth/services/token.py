"""JWT token provider implementation.

This module provides JWT token creation and verification.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from app.domains.auth.domain.enums import UserRole
from app.domains.auth.domain.exceptions import (
    ExpiredTokenException,
    InvalidTokenException,
)


class JWTTokenProvider:
    """JWT-based token provider implementation.

    This provider handles all JWT operations including creating access tokens,
    refresh tokens, and verifying token validity.

    Attributes:
        secret_key: Secret key for JWT signing
        algorithm: Algorithm used for JWT signing (default: HS256)
        access_token_expire_minutes: Access token expiration time in minutes
        refresh_token_expire_days: Refresh token expiration time in days
    """

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7,
    ) -> None:
        """Initialize JWT token provider.

        Args:
            secret_key: Secret key for JWT signing
            algorithm: Algorithm for JWT signing (default: HS256)
            access_token_expire_minutes: Access token expiration in minutes
            refresh_token_expire_days: Refresh token expiration in days
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(self, user_id: str, email: str, role: UserRole) -> str:
        """Create a JWT access token.

        Args:
            user_id: User's unique identifier (ULID)
            email: User's email address
            role: User's role in the system

        Returns:
            Encoded JWT access token string
        """
        expires_at = datetime.now(UTC) + timedelta(
            minutes=self.access_token_expire_minutes
        )

        payload = {
            "sub": user_id,  # Subject (user ID)
            "email": email,
            "role": role,  # StrEnum serializes directly as string
            "type": "access",
            "exp": expires_at,
            "iat": datetime.now(UTC),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """Create a JWT refresh token.

        Refresh tokens have fewer claims and longer expiration.

        Args:
            user_id: User's unique identifier (ULID)

        Returns:
            Encoded JWT refresh token string
        """
        expires_at = datetime.now(UTC) + timedelta(days=self.refresh_token_expire_days)

        payload = {
            "sub": user_id,  # Subject (user ID)
            "type": "refresh",
            "exp": expires_at,
            "iat": datetime.now(UTC),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict[str, Any]:
        """Verify and decode a JWT token.

        Args:
            token: JWT token string to verify

        Returns:
            Decoded token payload as dictionary

        Raises:
            InvalidTokenException: If token is invalid or malformed
            ExpiredTokenException: If token has expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError as e:
            raise ExpiredTokenException() from e
        except JWTError as e:
            raise InvalidTokenException() from e

    def decode_token(self, token: str) -> dict[str, Any]:
        """Decode a JWT token without verification (for debugging).

        Args:
            token: JWT token string to decode

        Returns:
            Decoded token payload as dictionary (may be invalid/expired)
        """
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
            options={"verify_signature": False, "verify_exp": False},
        )
