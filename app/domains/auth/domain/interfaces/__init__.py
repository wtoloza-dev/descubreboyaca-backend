"""Auth domain interfaces.

This module contains interface contracts for the auth domain.
"""

from app.domains.auth.domain.interfaces.oauth_client import OAuthClient
from app.domains.auth.domain.interfaces.password_hasher import PasswordHasher
from app.domains.auth.domain.interfaces.token_provider import TokenProvider
from app.domains.auth.domain.interfaces.user_repository import (
    UserRepositoryInterface,
)


__all__ = [
    "UserRepositoryInterface",
    "TokenProvider",
    "PasswordHasher",
    "OAuthClient",
]
