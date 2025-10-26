"""Shared dependencies for dependency injection.

This module exports all shared dependencies that can be used across domains.
All dependency functions follow the naming convention: get_{entity}_{type}_dependency
"""

from app.shared.dependencies.archive import (
    get_async_archive_repository_dependency,
    get_async_archive_service_dependency,
)
from app.shared.dependencies.pagination import get_pagination_params_dependency
from app.shared.dependencies.sql import get_async_session_dependency


__all__ = [
    "get_async_session_dependency",
    "get_async_archive_repository_dependency",
    "get_async_archive_service_dependency",
    "get_pagination_params_dependency",
]
