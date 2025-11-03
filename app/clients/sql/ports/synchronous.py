"""SQL client port for synchronous operations (Port).

This module defines the Port interface for synchronous SQL database clients.
This is a PORT in Hexagonal Architecture (Clean Architecture).

Best Practices:
    - Engine lifecycle is managed by FastAPI lifespan events
    - Adapters are initialized once on startup and reused
    - Sessions are created per-request via dependency injection
    - No manual close() needed - engines dispose automatically on shutdown
"""

from collections.abc import Generator
from typing import Protocol

from sqlmodel import Session


class SQLClientPort(Protocol):
    """Port defining the contract for synchronous SQL database clients.

    This is the PORT in Hexagonal Architecture. Any SQL client implementation
    (SQLite, PostgreSQL, MySQL, etc.) must implement this interface.

    The client only provides session management. All database operations
    should be performed using the session in repositories.
    """

    def get_session(self) -> Generator[Session]:
        """Get a database session context manager.

        Yields:
            Session: SQLModel session for database operations

        Example:
            >>> with client.get_session() as session:
            ...     restaurant = session.exec(select(Restaurant)).first()
            ...     session.add(new_restaurant)
            ...     session.commit()
        """
        ...
