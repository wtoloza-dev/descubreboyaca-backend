"""Common restaurant schemas - BASE CLASSES ONLY.

This module contains BASE schemas meant for inheritance.
Do NOT import these directly in your routes or other modules.

Each layer (admin, owner, public) should define its own specific schemas
that inherit from these base classes.
"""

from .ownership import BaseOwnershipSchema


__all__ = [
    "BaseOwnershipSchema",
]
