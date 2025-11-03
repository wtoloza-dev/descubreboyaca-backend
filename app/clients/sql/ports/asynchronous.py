"""SQL client port for asynchronous operations (Port).

This module defines the Port interface for asynchronous SQL database clients.
This is a PORT in Hexagonal Architecture (Clean Architecture).

Best Practices:
    - Engine lifecycle is managed by FastAPI lifespan events
    - Adapters are initialized once on startup and reused
    - Sessions are created per-request via dependency injection
    - No manual close() needed - engines dispose automatically on shutdown
"""

from typing import Protocol

from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncSQLClientPort(Protocol):
    """Port defining the contract for asynchronous SQL database clients.

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
