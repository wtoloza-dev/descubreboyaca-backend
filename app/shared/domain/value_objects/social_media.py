"""Social media value object.

This module defines the SocialMedia value object for managing social media links.
"""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from app.shared.domain.enums import SocialMediaPlatform


class SocialMedia(BaseModel):
    """Social media links value object.

    Represents a collection of social media profile URLs.
    This is an immutable value object that can be shared across domains.

    Attributes:
        facebook: Facebook profile URL
        instagram: Instagram profile URL
        twitter: Twitter/X profile URL
        tiktok: TikTok profile URL
        youtube: YouTube channel URL
        whatsapp: WhatsApp business link

    Example:
        >>> social = SocialMedia(
        ...     facebook="https://facebook.com/restaurant",
        ...     instagram="https://instagram.com/restaurant",
        ... )
    """

    model_config = ConfigDict(frozen=True)

    facebook: HttpUrl | None = Field(default=None, description="Facebook profile URL")
    instagram: HttpUrl | None = Field(default=None, description="Instagram profile URL")
    twitter: HttpUrl | None = Field(default=None, description="Twitter/X profile URL")
    tiktok: HttpUrl | None = Field(default=None, description="TikTok profile URL")
    youtube: HttpUrl | None = Field(default=None, description="YouTube channel URL")
    whatsapp: str | None = Field(
        default=None,
        description="WhatsApp business link or phone number",
        max_length=100,
    )

    @field_validator("whatsapp", mode="before")
    @classmethod
    def validate_whatsapp(cls, v: str | None) -> str | None:
        """Validate WhatsApp link or phone number.

        Args:
            v: WhatsApp link or phone number

        Returns:
            Validated WhatsApp link or None

        Raises:
            ValueError: If format is invalid
        """
        if v is None or v.strip() == "":
            return None

        v = v.strip()

        # Allow WhatsApp URLs
        if v.startswith("https://wa.me/") or v.startswith("https://api.whatsapp.com/"):
            return v

        # Allow phone numbers (basic validation)
        if v.startswith("+") and len(v) >= 10:
            return v

        msg = "WhatsApp must be a valid URL (https://wa.me/...) or phone number starting with +"
        raise ValueError(msg)

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary with only non-null values.

        Returns:
            Dictionary with social media platforms and their URLs
        """
        return {
            key: str(value) for key, value in self.model_dump(exclude_none=True).items()
        }

    def has_any_link(self) -> bool:
        """Check if any social media link is set.

        Returns:
            True if at least one social media link exists, False otherwise
        """
        return any(
            [
                self.facebook,
                self.instagram,
                self.twitter,
                self.tiktok,
                self.youtube,
                self.whatsapp,
            ]
        )

    @classmethod
    def get_supported_platforms(cls) -> list[str]:
        """Get list of supported social media platforms.

        Returns:
            List of platform names

        Example:
            >>> SocialMedia.get_supported_platforms()
            ['facebook', 'instagram', 'twitter', 'tiktok', 'youtube', 'whatsapp']
        """
        return SocialMediaPlatform.get_all()
