"""OAuth profile domain value object.

This module defines the OAuthProfile value object for storing OAuth2 provider data.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.domains.users.domain.enums import AuthProvider


class OAuthProfile(BaseModel):
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

    model_config = ConfigDict(frozen=True)

    provider: AuthProvider = Field(description="OAuth2 provider")
    provider_user_id: str = Field(description="Unique user ID from provider")
    email: str = Field(description="User's email from provider")
    full_name: str = Field(description="User's full name from provider")
    profile_picture_url: str | None = Field(
        default=None, description="URL to user's profile picture"
    )
    email_verified: bool = Field(
        default=False, description="Whether email is verified by provider"
    )

    def __str__(self) -> str:
        """Return string representation.

        Returns:
            String representation of the OAuth profile
        """
        return f"OAuthProfile(provider={self.provider.value}, email={self.email})"

    def __repr__(self) -> str:
        """Return developer-friendly representation.

        Returns:
            Detailed representation of the OAuth profile
        """
        return (
            f"OAuthProfile(provider={self.provider.value}, "
            f"provider_user_id={self.provider_user_id}, "
            f"email={self.email}, "
            f"full_name={self.full_name}, "
            f"email_verified={self.email_verified})"
        )
