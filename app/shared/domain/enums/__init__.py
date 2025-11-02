"""Shared enums.

This package contains enumerations shared across multiple bounded contexts.
Enums represent fixed sets of named constants.
"""

from .perception import Perception
from .social_media_platform import SocialMediaPlatform


__all__ = [
    "Perception",
    "SocialMediaPlatform",
]
