"""Token provider interface.

This module defines the interface contract for JWT token operations.
"""

from typing import Any, Protocol

from app.domains.auth.domain.enums import UserRole


class TokenProvider(Protocol):
    """Interface defining the contract for JWT token provider.

    This interface defines the operations for creating and verifying JWT tokens.
    """

    def create_access_token(self, user_id: str, email: str, role: UserRole) -> str:
        """Create a JWT access token.

        Args:
            user_id: User's unique identifier (ULID)
            email: User's email address
            role: User's role in the system

        Returns:
            Encoded JWT access token string
        """
        ...

    def create_refresh_token(self, user_id: str) -> str:
        """Create a JWT refresh token.

        Args:
            user_id: User's unique identifier (ULID)

        Returns:
            Encoded JWT refresh token string
        """
        ...

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
        ...

    def decode_token(self, token: str) -> dict[str, Any]:
        """Decode a JWT token without verification (for debugging).

        Args:
            token: JWT token string to decode

        Returns:
            Decoded token payload as dictionary (may be invalid/expired)
        """
        ...
