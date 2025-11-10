"""Auth domain module.

This module contains the core domain logic for authentication and authorization.
User entity has been moved to users domain as it owns the user lifecycle.
"""

from app.domains.auth.domain.exceptions import (
    AuthenticationException,
    ExpiredTokenException,
    InsufficientPermissionsException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from app.domains.auth.domain.interfaces import (
    OAuthClient,
    PasswordHasher,
    TokenProvider,
)
from app.domains.auth.domain.value_objects import (
    Credentials,
    OAuthProfile,
    PasswordHash,
    Token,
    TokenData,
)


__all__ = [
    # Exceptions
    "AuthenticationException",
    "InvalidCredentialsException",
    "InvalidTokenException",
    "ExpiredTokenException",
    "InsufficientPermissionsException",
    # Interfaces
    "PasswordHasher",
    "TokenProvider",
    "OAuthClient",
    # Value Objects
    "Credentials",
    "Token",
    "TokenData",
    "PasswordHash",
    "OAuthProfile",
]
