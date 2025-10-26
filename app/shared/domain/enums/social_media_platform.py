"""Social media platforms enumeration.

This module defines the supported social media platforms as an enum
to prevent typos and provide documentation.
"""

from enum import StrEnum


class SocialMediaPlatform(StrEnum):
    """Supported social media platforms.

    This enum documents all social media platforms supported by the system.
    Using an enum prevents typos and provides IDE autocomplete.

    Attributes:
        FACEBOOK: Facebook social network
        INSTAGRAM: Instagram photo/video sharing
        TWITTER: Twitter/X microblogging
        TIKTOK: TikTok video sharing
        YOUTUBE: YouTube video platform
        WHATSAPP: WhatsApp messaging (business)
    """

    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    WHATSAPP = "whatsapp"

    @classmethod
    def get_all(cls) -> list[str]:
        """Get all platform names as strings.

        Returns:
            List of all supported platform names
        """
        return [platform for platform in cls]

    @classmethod
    def is_valid(cls, platform: str) -> bool:
        """Check if a platform name is valid.

        Args:
            platform: Platform name to validate

        Returns:
            True if platform is supported, False otherwise
        """
        return platform in cls.get_all()
