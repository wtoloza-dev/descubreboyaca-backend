"""SQL client dependency factories.

This package provides factory functions to create SQL client instances
with different configurations. This allows having multiple instances
of the same client type (e.g., multiple database connections for
different databases or purposes).

This follows the Dependency Injection pattern and acts as the application's
composition root for database clients.
"""

from .sqlite import (
    get_async_sqlite_client_dependency,
    get_async_sqlite_session_dependency,
    get_sqlite_client_dependency,
    get_sqlite_session_dependency,
)


__all__ = [
    "get_sqlite_client_dependency",
    "get_async_sqlite_client_dependency",
    "get_sqlite_session_dependency",
    "get_async_sqlite_session_dependency",
]
