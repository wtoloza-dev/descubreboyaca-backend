"""SQL adapter factory functions.

This package provides generic factory functions to create SQL adapter instances.
These factories are app-agnostic and accept all configuration as parameters.

These adapters are typically created once during application startup in the lifespan
and shared across all requests for optimal connection pooling.

For session dependencies, use get_session/get_async_session from app.shared.dependencies.sql
"""

from .postgres import (
    create_async_postgres_adapter,
    create_postgres_adapter,
)
from .sqlite import (
    create_async_sqlite_adapter,
    create_sqlite_adapter,
)


__all__ = [
    "create_sqlite_adapter",
    "create_async_sqlite_adapter",
    "create_postgres_adapter",
    "create_async_postgres_adapter",
]
