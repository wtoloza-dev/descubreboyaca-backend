"""Auth domain interfaces.

This module contains interface contracts for the auth domain.
UserRepositoryInterface has been moved to users domain.
"""

from app.domains.auth.domain.interfaces.oauth_client import OAuthClient
from app.domains.auth.domain.interfaces.password_hasher import PasswordHasher
from app.domains.auth.domain.interfaces.token_provider import TokenProvider


__all__ = [
    "TokenProvider",
    "PasswordHasher",
    "OAuthClient",
]
