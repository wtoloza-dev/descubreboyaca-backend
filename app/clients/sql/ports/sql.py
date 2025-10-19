"""SQL client protocol for synchronous operations (Port).

This module defines the Protocol interface for synchronous SQL database clients.
This is a PORT in Hexagonal Architecture (Clean Architecture).
"""

from collections.abc import Generator
from typing import Protocol

from sqlmodel import Session


class SQLClientProtocol(Protocol):
    """Protocol defining the contract for synchronous SQL database clients.

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

    def create_db_and_tables(self) -> None:
        """Create all database tables defined in SQLModel models.

        This should be called during application startup to initialize the database.

        Example:
            >>> client.create_db_and_tables()
        """
        ...

    def close(self) -> None:
        """Close the database connection and dispose of the engine.

        Should be called during application shutdown.

        Example:
            >>> client.close()
        """
        ...
