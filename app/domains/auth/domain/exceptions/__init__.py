"""Auth domain exceptions.

This module contains domain-specific exceptions for authentication.
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
from app.domains.auth.domain.exceptions.user_already_exists import (
    UserAlreadyExistsException,
)
from app.domains.auth.domain.exceptions.user_inactive import UserInactiveException
from app.domains.auth.domain.exceptions.user_not_found import UserNotFoundException


__all__ = [
    "AuthenticationException",
    "InvalidCredentialsException",
    "UserAlreadyExistsException",
    "UserNotFoundException",
    "InvalidTokenException",
    "ExpiredTokenException",
    "UserInactiveException",
    "InsufficientPermissionsException",
]
