"""Authentication provider enumeration.

This module defines the authentication providers supported by the system.
"""

from enum import StrEnum


class AuthProvider(StrEnum):
    """Authentication provider enumeration.

    Defines the authentication methods/providers supported by the system.

    Attributes:
        EMAIL: Email and password authentication
        GOOGLE: Google OAuth2 authentication
        FACEBOOK: Facebook OAuth2 authentication (future support)
    """

    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"
