"""Auth domain entities following DDD principles.

This module contains core business entities for the auth domain.
"""

from app.domains.auth.domain.entities.user import User, UserData


__all__ = [
    "User",
    "UserData",
]
