"""Google OAuth client implementation.

This module provides Google OAuth2 authentication functionality.
"""

from typing import Any

import httpx

from app.domains.auth.domain.exceptions import AuthenticationException
from app.domains.auth.domain.value_objects import OAuthProfile
from app.domains.users.domain.enums import AuthProvider


class GoogleOAuthClient:
    """Client for Google OAuth2 authentication.

    This client handles the OAuth2 flow with Google, including
    generating authorization URLs and exchanging codes for user profiles.

    Attributes:
        client_id: Google OAuth client ID
        client_secret: Google OAuth client secret
        redirect_uri: Redirect URI registered in Google Console
        scopes: OAuth scopes requested
    """

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: list[str] | None = None,
    ) -> None:
        """Initialize Google OAuth client.

        Args:
            client_id: Google OAuth client ID
            client_secret: Google OAuth client secret
            redirect_uri: Redirect URI for OAuth callback
            scopes: OAuth scopes to request (default: email, profile, openid)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes or [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]

    def get_authorization_url(self) -> str:
        """Get the Google OAuth2 authorization URL for user redirect.

        Returns:
            Authorization URL where user should be redirected
        """
        scope_string = " ".join(self.scopes)
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": scope_string,
            "access_type": "offline",  # Request refresh token
            "prompt": "consent",  # Force consent screen
        }

        # Build URL with query parameters
        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{self.GOOGLE_AUTH_URL}?{query_string}"

    async def get_user_profile(self, code: str) -> OAuthProfile:
        """Get user profile from Google using authorization code.

        This method exchanges the authorization code for an access token,
        then uses the access token to fetch the user's profile.

        Args:
            code: Authorization code from OAuth2 callback

        Returns:
            OAuthProfile with user data from Google

        Raises:
            AuthenticationException: If unable to get profile from Google
        """
        try:
            # Exchange code for access token
            access_token = await self._exchange_code_for_token(code)

            # Get user profile using access token
            profile = await self._get_google_profile(access_token)

            return profile

        except httpx.HTTPError as e:
            raise AuthenticationException(
                f"Failed to authenticate with Google: {e!s}"
            ) from e

    async def verify_token(self, token: str) -> OAuthProfile:
        """Verify Google OAuth2 token and get user profile.

        Args:
            token: Google OAuth2 access token to verify

        Returns:
            OAuthProfile with user data from Google

        Raises:
            AuthenticationException: If token is invalid
        """
        return await self._get_google_profile(token)

    async def _exchange_code_for_token(self, code: str) -> str:
        """Exchange authorization code for access token.

        Args:
            code: Authorization code from Google

        Returns:
            Access token string

        Raises:
            AuthenticationException: If token exchange fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "authorization_code",
                },
            )

            if response.status_code != 200:
                raise AuthenticationException(
                    f"Failed to exchange code for token: {response.text}"
                )

            token_data = response.json()
            return token_data["access_token"]

    async def _get_google_profile(self, access_token: str) -> OAuthProfile:
        """Get user profile from Google using access token.

        Args:
            access_token: Google OAuth access token

        Returns:
            OAuthProfile with user data

        Raises:
            AuthenticationException: If unable to fetch profile
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if response.status_code != 200:
                raise AuthenticationException(
                    f"Failed to get user profile from Google: {response.text}"
                )

            user_data: dict[str, Any] = response.json()

            return OAuthProfile(
                provider=AuthProvider.GOOGLE,
                provider_user_id=user_data["id"],
                email=user_data["email"],
                full_name=user_data.get("name", ""),
                profile_picture_url=user_data.get("picture"),
                email_verified=user_data.get("verified_email", False),
            )
