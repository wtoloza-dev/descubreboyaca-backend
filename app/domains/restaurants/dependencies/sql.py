"""SQL dependencies for the restaurants domain.

This module provides dependency functions for the restaurants domain.
"""

from collections.abc import AsyncGenerator, Generator

from sqlmodel import AsyncSession, Session

from app.clients.sql.dependencies import (
    get_async_sqlite_session_dependency,
    get_sqlite_session_dependency,
)
from app.core.settings import settings


def get_restaurant_session_dependency() -> Generator[Session]:
    """Dependency to get a SQLite session for the restaurants domain.

    Yields:
        Session: SQLite session for the restaurants domain.
    """
    if settings.SCOPE == "local":
        return get_sqlite_session_dependency()
    else:
        raise NotImplementedError("SQLite session dependency not implemented")


def get_restaurant_async_session_dependency() -> AsyncGenerator[AsyncSession]:
    """Dependency to get an async SQLite session for the restaurants domain.

    Yields:
        AsyncSession: Async SQLite session for the restaurants domain.
    """
    if settings.SCOPE == "local":
        return get_async_sqlite_session_dependency()
    else:
        raise NotImplementedError("Async SQLite session dependency not implemented")
