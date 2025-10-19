"""Shared dependencies.

This package provides factory functions for shared components
like archive service, repositories, etc.

These are simple factory functions that construct instances.
Only routes should use Depends() to inject the Session.
"""

from app.shared.dependencies.archive import (
    get_archive_repository,
    get_archive_service,
    get_async_archive_repository,
    get_async_archive_service,
)


__all__ = [
    "get_archive_repository",
    "get_async_archive_repository",
    "get_archive_service",
    "get_async_archive_service",
]
