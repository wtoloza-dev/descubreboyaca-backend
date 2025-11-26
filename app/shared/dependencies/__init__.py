"""Shared dependencies for dependency injection.

This module exports all shared dependencies that can be used across domains.
All dependency functions follow the naming convention: get_{entity}_{type}_dependency

Note: Archive dependencies have been moved to app/domains/audit/dependencies/
"""

from app.shared.dependencies.observability import get_metrics_client_dependency
from app.shared.dependencies.pagination import get_pagination_dependency
from app.shared.dependencies.sql import (
    get_async_session_dependency,
    get_session_dependency,
)


__all__ = [
    "get_async_session_dependency",
    "get_session_dependency",
    "get_pagination_dependency",
    "get_metrics_client_dependency",
]
