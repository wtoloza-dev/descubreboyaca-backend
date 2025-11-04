"""Audit dependency injection."""

from .archive import (
    get_archive_repository_dependency,
    get_archive_service_dependency,
)


__all__ = [
    "get_archive_repository_dependency",
    "get_archive_service_dependency",
]
