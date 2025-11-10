"""Auth domain exceptions.

This module contains exception classes for the auth domain.
User-related exceptions have been moved to users domain.
"""

from app.domains.auth.domain.exceptions.authentication import AuthenticationException
from app.domains.auth.domain.exceptions.expired_token import ExpiredTokenException
from app.domains.auth.domain.exceptions.insufficient_permissions import (
    InsufficientPermissionsException,
)
from app.domains.auth.domain.exceptions.invalid_credentials import (
    InvalidCredentialsException,
)
from app.domains.auth.domain.exceptions.invalid_token import InvalidTokenException


__all__ = [
    "AuthenticationException",
    "InvalidCredentialsException",
    "InvalidTokenException",
    "ExpiredTokenException",
    "InsufficientPermissionsException",
]
