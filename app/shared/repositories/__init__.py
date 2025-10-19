"""Shared repositories.

This package contains repository implementations for shared domain entities.
Repositories handle data persistence and retrieval.
"""

from app.shared.repositories.archive import (
    ArchiveRepository,
    AsyncArchiveRepository,
)


__all__ = ["ArchiveRepository", "AsyncArchiveRepository"]
