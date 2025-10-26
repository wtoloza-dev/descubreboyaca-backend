"""Shared value objects.

This package contains value objects shared across multiple bounded contexts.
Value Objects are immutable objects that represent descriptive aspects
of the domain with no conceptual identity.
"""

from .geolocation import GeoLocation
from .pagination import PaginationParams
from .social_media import SocialMedia


__all__ = [
    "GeoLocation",
    "PaginationParams",
    "SocialMedia",
]
