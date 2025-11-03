"""SQL adapter dependency factories.

This package provides generic factory functions to create SQL adapter
instances. These factories are app-agnostic and accept all configuration
as parameters.

For app-specific configurations that use settings, use the factories
in app.shared.dependencies instead.
"""

from .sqlite import (
    create_async_sqlite_adapter,
    create_async_sqlite_session_dependency,
    create_sqlite_adapter,
    create_sqlite_session_dependency,
)


__all__ = [
    "create_sqlite_adapter",
    "create_async_sqlite_adapter",
    "create_sqlite_session_dependency",
    "create_async_sqlite_session_dependency",
]
