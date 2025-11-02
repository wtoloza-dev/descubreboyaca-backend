"""OAuth client interface.

This module defines the interface contract for OAuth2 operations.
"""

from typing import Protocol

from app.domains.auth.domain.value_objects import OAuthProfile


class OAuthClient(Protocol):
    """Interface defining the contract for OAuth2 client.

    This interface defines the operations for OAuth2 authentication flows.
    """

    def get_authorization_url(self) -> str:
        """Get the OAuth2 authorization URL for user redirect.

        Returns:
            Authorization URL where user should be redirected
        """
        ...

    async def get_user_profile(self, code: str) -> OAuthProfile:
        """Get user profile from OAuth2 provider using authorization code.

        Args:
            code: Authorization code from OAuth2 callback

        Returns:
            OAuthProfile with user data from the provider

        Raises:
            AuthenticationException: If unable to get profile from provider
        """
        ...

    async def verify_token(self, token: str) -> OAuthProfile:
        """Verify OAuth2 token and get user profile.

        Args:
            token: OAuth2 access token to verify

        Returns:
            OAuthProfile with user data from the provider

        Raises:
            AuthenticationException: If token is invalid
        """
        ...
