"""Auth domain value objects.

This module contains immutable value objects for the auth domain.
"""

from app.domains.auth.domain.value_objects.create_user_data import CreateUserData
from app.domains.auth.domain.value_objects.credentials import Credentials
from app.domains.auth.domain.value_objects.oauth_profile import OAuthProfile
from app.domains.auth.domain.value_objects.password import PasswordHash
from app.domains.auth.domain.value_objects.token import Token, TokenData


__all__ = [
    "CreateUserData",
    "Credentials",
    "OAuthProfile",
    "PasswordHash",
    "Token",
    "TokenData",
]
