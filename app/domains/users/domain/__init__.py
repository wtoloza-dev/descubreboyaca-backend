"""Users domain module.

This module contains the core domain logic for user management.
"""

from app.domains.users.domain.entities import User, UserData
from app.domains.users.domain.enums import AuthProvider, UserRole
from app.domains.users.domain.exceptions import (
    UserAlreadyExistsException,
    UserInactiveException,
    UserNotFoundException,
)
from app.domains.users.domain.interfaces import UserRepositoryInterface
from app.domains.users.domain.value_objects import CreateUserData


__all__ = [
    # Entities
    "User",
    "UserData",
    # Enums
    "UserRole",
    "AuthProvider",
    # Exceptions
    "UserNotFoundException",
    "UserAlreadyExistsException",
    "UserInactiveException",
    # Interfaces
    "UserRepositoryInterface",
    # Value Objects
    "CreateUserData",
]
