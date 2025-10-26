"""OAuth profile domain entity.

This module defines the OAuthProfile entity for storing OAuth2 provider data.
"""

from dataclasses import dataclass

from app.domains.auth.domain.enums.auth_provider import AuthProvider


@dataclass(frozen=True)
class OAuthProfile:
    """Immutable OAuth2 profile data from external providers.

    This represents user profile data received from OAuth2 providers
    like Google, Facebook, etc. Being frozen ensures data integrity.

    Attributes:
        provider: OAuth2 provider (google, facebook, etc.)
        provider_user_id: Unique user ID from the provider
        email: User's email from the provider
        full_name: User's full name from the provider
        profile_picture_url: URL to user's profile picture
        email_verified: Whether the email is verified by the provider
    """

    provider: AuthProvider
    provider_user_id: str
    email: str
    full_name: str
    profile_picture_url: str | None = None
    email_verified: bool = False
