"""Shared domain entities.

This package contains domain entities shared across multiple bounded contexts.
Entities are objects with identity and lifecycle.
"""

from .archive import Archive, ArchiveData
from .audit import Audit


__all__ = [
    "Archive",
    "ArchiveData",
    "Audit",
]
