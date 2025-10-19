"""Shared domain interfaces.

This package contains abstract interfaces and protocols shared across multiple domains,
defining contracts for repositories and services.
"""

from app.shared.interfaces.archive import (
    ArchiveRepositoryProtocol,
    AsyncArchiveRepositoryProtocol,
)


__all__ = ["ArchiveRepositoryProtocol", "AsyncArchiveRepositoryProtocol"]
