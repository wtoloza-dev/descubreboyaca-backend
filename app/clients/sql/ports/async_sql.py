"""SQL client protocol for asynchronous operations (Port).

This module defines the Protocol interface for asynchronous SQL database clients.
This is a PORT in Hexagonal Architecture (Clean Architecture).
"""

from typing import Protocol

from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncSQLClientProtocol(Protocol):
    """Protocol defining the contract for asynchronous SQL database clients.

    This is the PORT in Hexagonal Architecture. Any async SQL client implementation
    (AsyncSQLite, AsyncPostgreSQL, etc.) must implement this interface.

    The client only provides session management. All database operations
    should be performed using the async session in repositories.
    """

    async def get_session(self) -> AsyncSession:
        """Get an async database session context manager.

        Yields:
            AsyncSession: SQLModel async session for database operations

        Example:
            >>> async with client.get_session() as session:
            ...     result = await session.exec(select(Restaurant))
            ...     restaurant = result.first()
            ...     session.add(new_restaurant)
            ...     await session.commit()
        """
        ...

    async def create_db_and_tables(self) -> None:
        """Create all database tables defined in SQLModel models.

        This should be called during application startup to initialize the database.

        Example:
            >>> await client.create_db_and_tables()
        """
        ...

    async def close(self) -> None:
        """Close the database connection and dispose of the engine.

        Should be called during application shutdown.

        Example:
            >>> await client.close()
        """
        ...
