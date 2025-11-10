"""Common restaurant schemas shared across admin, owner, and public endpoints."""

from .ownership import OwnershipSchemaResponse


__all__ = [
    "OwnershipSchemaResponse",
]
