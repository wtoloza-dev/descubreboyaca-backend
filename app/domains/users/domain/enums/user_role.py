"""User role enumeration.

This module defines the roles available for users in the system.
"""

from enum import StrEnum


class UserRole(StrEnum):
    """User role enumeration.

    Defines the available roles for users in the system.
    Each role has different permissions and access levels.

    Attributes:
        ADMIN: Administrator with full system access
        OWNER: Restaurant owner with business management permissions
        USER: Regular user with standard permissions
        GUEST: Guest user with limited permissions
    """

    ADMIN = "admin"
    OWNER = "owner"
    USER = "user"
    GUEST = "guest"
