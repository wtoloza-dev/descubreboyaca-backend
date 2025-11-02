"""Audit dependency injection."""

from .archive import (
    get_async_archive_repository_dependency,
    get_async_archive_service_dependency,
)


__all__ = [
    "get_async_archive_repository_dependency",
    "get_async_archive_service_dependency",
]

