"""Shared domain entities.

This package contains the core business entities shared across multiple domains.
Entities represent objects with identity and lifecycle.
"""

from app.shared.entities.archive import Archive, ArchiveData
from app.shared.entities.audit import Audit


__all__ = [
    "Archive",
    "ArchiveData",
    "Audit",
]
