"""SQLite synchronous database adapter (Adapter).

This module provides synchronous implementation for SQLite databases.
This is an ADAPTER in Hexagonal Architecture.
"""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlmodel import Session


class SQLiteSynchronousAdapter:
    """SQLite synchronous database adapter implementation.

    This adapter implements the SQLClientPort for SQLite databases.
    It handles connection management and session lifecycle.

    All database operations (queries, inserts, updates, deletes) should be
    performed directly on the session in repositories.

    Attributes:
        engine: SQLAlchemy engine for database connections

    Example:
        >>> adapter = SQLiteSynchronousAdapter("sqlite:///./database.db")
        >>> with adapter.get_session() as session:
        ...     # Query
        ...     restaurants = session.exec(select(Restaurant)).all()
        ...     # Insert
        ...     session.add(new_restaurant)
        ...     session.commit()
    """

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize SQLite adapter.

        Args:
            database_url: SQLite database URL (e.g., "sqlite:///./database.db")
            echo: Whether to echo SQL statements (useful for debugging)

        Example:
            >>> adapter = SQLiteSynchronousAdapter("sqlite:///./app.db", echo=True)
        """
        self.engine: Engine = create_engine(
            database_url,
            echo=echo,
            connect_args={"check_same_thread": False},  # SQLite specific
        )

    @contextmanager
    def get_session(self) -> Generator[Session]:
        """Get a database session context manager.

        Yields:
            Session: SQLModel session for database operations

        Example:
            >>> with adapter.get_session() as session:
            ...     restaurant = session.exec(select(Restaurant)).first()
            ...     session.add(new_restaurant)
            ...     session.commit()
        """
        session = Session(self.engine)
        try:
            yield session
        finally:
            session.close()
