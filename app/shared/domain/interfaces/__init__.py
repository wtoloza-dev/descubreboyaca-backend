"""Shared domain interfaces.

This package contains abstract interfaces and protocols shared across multiple domains,
defining contracts for repositories and services.
"""

from .archive import (
    ArchiveRepositoryInterface,
    AsyncArchiveRepositoryInterface,
)


__all__ = [
    "ArchiveRepositoryInterface",
    "AsyncArchiveRepositoryInterface",
]
