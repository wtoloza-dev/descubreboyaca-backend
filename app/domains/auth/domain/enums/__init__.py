"""Auth domain enumerations.

This module contains enumerations for the auth domain.
"""

from app.domains.auth.domain.enums.auth_provider import AuthProvider
from app.domains.auth.domain.enums.user_role import UserRole


__all__ = [
    "UserRole",
    "AuthProvider",
]
