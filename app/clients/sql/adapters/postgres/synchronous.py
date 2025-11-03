"""PostgreSQL synchronous database adapter (Adapter).

This module provides synchronous implementation for PostgreSQL databases.
This is an ADAPTER in Hexagonal Architecture.
"""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine, create_engine
from sqlmodel import Session


class PostgreSQLSynchronousAdapter:
    """PostgreSQL synchronous database adapter implementation.

    This adapter implements the SQLClientPort for PostgreSQL databases.
    It handles connection management and session lifecycle with connection pooling.

    All database operations (queries, inserts, updates, deletes) should be
    performed directly on the session in repositories.

    Attributes:
        engine: SQLAlchemy engine for database connections

    Example:
        >>> adapter = PostgreSQLSynchronousAdapter(
        ...     "postgresql://user:pass@localhost/dbname"
        ... )
        >>> with adapter.get_session() as session:
        ...     # Query
        ...     restaurants = session.exec(select(Restaurant)).all()
        ...     # Insert
        ...     session.add(new_restaurant)
        ...     session.commit()
    """

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize PostgreSQL adapter.

        Args:
            database_url: PostgreSQL database URL
                Format: "postgresql://username:password@host:port/database"
            echo: Whether to echo SQL statements (useful for debugging)

        Example:
            >>> url = "postgresql://myuser:mypass@localhost:5432/mydb"
            >>> adapter = PostgreSQLSynchronousAdapter(url, echo=True)
        """
        self.engine: Engine = create_engine(
            database_url,
            echo=echo,
            pool_pre_ping=True,  # Verify connections before using
            pool_size=5,  # Connection pool size
            max_overflow=10,  # Additional connections when pool is full
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
