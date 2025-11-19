# Adapters (Implementations)

## Purpose

Adapters are **concrete implementations** of ports for specific database technologies. They provide the **how** to the port's **what**, implementing database-specific connection logic while maintaining a consistent interface.

## Key Concept

In Hexagonal Architecture, adapters translate between the application's needs (defined by ports) and external systems (databases).

```
Port (Interface)
    │ implemented by
    ▼
┌─────────────────────────────────┐
│         Adapters                │  ◄── You are here
│  • PostgreSQLAdapter            │
│  • SQLiteAdapter                │
│  • MySQLAdapter (future)        │
└─────────────────────────────────┘
    │ connects to
    ▼
External Databases
```

## Available Adapters

| Adapter | Database | Use Case |
|---------|----------|----------|
| **AsyncPostgreSQLAdapter** | PostgreSQL | Production, Staging |
| **AsyncSQLiteAdapter** | SQLite | Development, Testing |
| **SyncPostgreSQLAdapter** | PostgreSQL | Synchronous operations (rare) |
| **SyncSQLiteAdapter** | SQLite | Synchronous operations (rare) |

## AsyncPostgreSQLAdapter

Implements `AsyncSQLClientPort` for PostgreSQL database.

### Implementation

```python
# app/clients/sql/adapters/postgres/asynchronous.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncPostgreSQLAdapter:
    """PostgreSQL adapter implementing AsyncSQLClientPort.

    Manages connections to PostgreSQL database using asyncpg driver.
    Configured for production-grade connection pooling and reliability.

    Attributes:
        database_url: PostgreSQL connection string
        echo: Whether to log SQL queries
        engine: SQLAlchemy async engine
    """

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
    ) -> None:
        """Initialize PostgreSQL adapter.

        Args:
            database_url: PostgreSQL connection URL
                Format: postgresql+asyncpg://user:pass@host:port/dbname
            echo: Enable SQL query logging (useful for debugging)
        """
        self.database_url = database_url
        self.echo = echo
        self.engine: AsyncEngine | None = None

    def connect(self) -> None:
        """Create PostgreSQL engine with connection pooling.

        Configuration:
            - asyncpg driver for async operations
            - Connection pool with pre-ping health checks
            - Automatic reconnection on connection failures
        """
        self.engine = create_async_engine(
            self.database_url,
            echo=self.echo,
            pool_pre_ping=True,  # Verify connections before using
            pool_size=5,         # Max 5 connections in pool
            max_overflow=10,     # Allow 10 overflow connections
        )

    async def disconnect(self) -> None:
        """Dispose PostgreSQL engine and close all connections."""
        if self.engine:
            await self.engine.dispose()
            self.engine = None

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get PostgreSQL session.

        Yields:
            AsyncSession: Database session with automatic transaction management

        Example:
            >>> async with adapter.get_session() as session:
            ...     result = await session.execute(query)
            ...     await session.commit()
        """
        if not self.engine:
            raise RuntimeError("Engine not initialized. Call connect() first.")

        async with AsyncSession(
            self.engine,
            expire_on_commit=False,  # Keep objects usable after commit
        ) as session:
            yield session
```

### PostgreSQL-Specific Features

**Connection Pooling**:
```python
pool_size=5          # Keep 5 persistent connections
max_overflow=10      # Create up to 10 extra connections if needed
```

**Health Checks**:
```python
pool_pre_ping=True   # Test connection before using (prevents stale connections)
```

**Asyncpg Driver**:
- High-performance async PostgreSQL driver
- Native async/await support
- Efficient connection management

## AsyncSQLiteAdapter

Implements `AsyncSQLClientPort` for SQLite database.

### Implementation

```python
# app/clients/sql/adapters/sqlite/asynchronous.py

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncSQLiteAdapter:
    """SQLite adapter implementing AsyncSQLClientPort.

    Manages connections to SQLite database using aiosqlite driver.
    Optimized for development and testing environments.

    Attributes:
        database_url: SQLite connection string
        echo: Whether to log SQL queries
        engine: SQLAlchemy async engine
    """

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
    ) -> None:
        """Initialize SQLite adapter.

        Args:
            database_url: SQLite connection URL
                Format: sqlite+aiosqlite:///path/to/db.db
                In-memory: sqlite+aiosqlite:///:memory:
            echo: Enable SQL query logging
        """
        self.database_url = database_url
        self.echo = echo
        self.engine: AsyncEngine | None = None

    def connect(self) -> None:
        """Create SQLite engine.

        Configuration:
            - aiosqlite driver for async operations
            - Check same thread disabled (required for async)
            - Foreign keys enforced
        """
        self.engine = create_async_engine(
            self.database_url,
            echo=self.echo,
            connect_args={"check_same_thread": False},  # Required for async
        )

    async def disconnect(self) -> None:
        """Dispose SQLite engine and close connection."""
        if self.engine:
            await self.engine.dispose()
            self.engine = None

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get SQLite session.

        Yields:
            AsyncSession: Database session

        Example:
            >>> async with adapter.get_session() as session:
            ...     result = await session.execute(query)
        """
        if not self.engine:
            raise RuntimeError("Engine not initialized. Call connect() first.")

        async with AsyncSession(self.engine) as session:
            yield session
```

### SQLite-Specific Features

**Thread Safety**:
```python
connect_args={"check_same_thread": False}  # Allow async usage
```

**In-Memory Database**:
```python
# For testing - database exists only in RAM
database_url = "sqlite+aiosqlite:///:memory:"
```

**File-Based Database**:
```python
# For development - persistent database file
database_url = "sqlite+aiosqlite:///./local.db"
```

## Synchronous Adapters

Similar implementations for synchronous operations (rarely used).

### SyncPostgreSQLAdapter

```python
# app/clients/sql/adapters/postgres/synchronous.py

from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlmodel import Session

class SyncPostgreSQLAdapter:
    """Synchronous PostgreSQL adapter."""

    def __init__(self, database_url: str, echo: bool = False):
        self.database_url = database_url
        self.echo = echo
        self.engine: Engine | None = None

    def connect(self) -> None:
        """Create sync engine."""
        self.engine = create_engine(
            self.database_url,
            echo=self.echo,
            pool_pre_ping=True,
        )

    def disconnect(self) -> None:
        """Dispose engine."""
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def get_session(self) -> Generator[Session, None, None]:
        """Get sync session."""
        if not self.engine:
            raise RuntimeError("Engine not initialized.")

        with Session(self.engine) as session:
            yield session
```

## Dependencies (Factories)

Factories select which adapter to use based on environment configuration.

### Async SQL Client Factory

```python
# app/clients/sql/dependencies/postgres.py

from typing import Annotated
from fastapi import Depends
from app.core.settings import settings
from app.clients.sql.ports import AsyncSQLClientPort
from app.clients.sql.adapters.postgres import AsyncPostgreSQLAdapter
from app.clients.sql.adapters.sqlite import AsyncSQLiteAdapter


def get_async_sql_client() -> AsyncSQLClientPort:
    """Factory to create async SQL client based on environment.

    Returns:
        AsyncSQLClientPort: PostgreSQL adapter for prod/staging,
                           SQLite adapter for local/testing

    Example:
        >>> # In production (SCOPE=prod)
        >>> client = get_async_sql_client()
        >>> # Returns: AsyncPostgreSQLAdapter

        >>> # In development (SCOPE=local)
        >>> client = get_async_sql_client()
        >>> # Returns: AsyncSQLiteAdapter
    """
    if settings.SCOPE == "local":
        return AsyncSQLiteAdapter(
            database_url=settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
        )
    else:
        return AsyncPostgreSQLAdapter(
            database_url=settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
        )
```

### Environment-Based Selection

| Environment | `SCOPE` Value | Adapter | Database |
|-------------|---------------|---------|----------|
| Development | `local` | AsyncSQLiteAdapter | SQLite file |
| Testing | `test` | AsyncSQLiteAdapter | In-memory SQLite |
| Staging | `staging` | AsyncPostgreSQLAdapter | PostgreSQL |
| Production | `prod` | AsyncPostgreSQLAdapter | PostgreSQL |

## Usage Flow

### 1. Application Startup

```python
# app/core/lifespan.py

from app.clients.sql.dependencies import get_async_sql_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Factory returns appropriate adapter
    client = get_async_sql_client()
    # Could be PostgreSQL or SQLite - doesn't matter!

    client.connect()
    logger.info(f"Connected to database ({client.__class__.__name__})")

    yield

    await client.disconnect()
```

### 2. Request Processing

```python
# app/shared/dependencies/sql.py

async def get_async_session_dependency(
    client: Annotated[AsyncSQLClientPort, Depends(get_async_sql_client)],
) -> AsyncGenerator[AsyncSession, None]:
    """Provide session to routes."""
    async with client.get_session() as session:
        yield session
```

### 3. Repository Usage

```python
# app/domains/restaurants/infrastructure/persistence/repositories/restaurant/postgresql.py

class PostgreSQLRestaurantRepository:
    def __init__(self, session: AsyncSession) -> None:
        """Session comes from adapter, but repository doesn't know which one."""
        self.session = session

    async def create(self, data: RestaurantData) -> Restaurant:
        """Works with any adapter that provides AsyncSession."""
        model = RestaurantModel(**data.model_dump())
        self.session.add(model)
        await self.session.commit()
        return self._to_entity(model)
```

## Testing Adapters

### Integration Test with SQLite

```python
# tests/integration/test_sqlite_adapter.py

import pytest
from app.clients.sql.adapters.sqlite import AsyncSQLiteAdapter

@pytest.fixture
async def sqlite_adapter():
    """Create in-memory SQLite adapter for testing."""
    adapter = AsyncSQLiteAdapter("sqlite+aiosqlite:///:memory:")
    adapter.connect()
    yield adapter
    await adapter.disconnect()

async def test_sqlite_session(sqlite_adapter):
    """Test SQLite adapter provides working session."""
    async with sqlite_adapter.get_session() as session:
        assert session is not None
        # Can execute queries
        result = await session.execute("SELECT 1")
        assert result is not None
```

### Integration Test with PostgreSQL

```python
# tests/integration/test_postgresql_adapter.py

@pytest.fixture
async def postgresql_adapter(test_database_url):
    """Create PostgreSQL adapter for testing."""
    adapter = AsyncPostgreSQLAdapter(test_database_url)
    adapter.connect()
    yield adapter
    await adapter.disconnect()

async def test_postgresql_connection(postgresql_adapter):
    """Test PostgreSQL adapter connects successfully."""
    async with postgresql_adapter.get_session() as session:
        result = await session.execute("SELECT version()")
        assert "PostgreSQL" in str(result.scalar())
```

## Key Principles

1. **Implement Port Contract** - All adapters implement the same port interface
2. **Hide Implementation Details** - Specific database features hidden from clients
3. **Environment-Based Selection** - Factory chooses adapter based on configuration
4. **Consistent Behavior** - All adapters provide the same functionality
5. **Resource Management** - Proper connection lifecycle (connect/disconnect)

## Benefits

| Benefit | Description |
|---------|-------------|
| **Swappable** | Change database by changing factory, not code |
| **Testable** | Use SQLite in tests, PostgreSQL in production |
| **Maintainable** | Database logic isolated in adapters |
| **Scalable** | Add new databases without changing existing code |

## Related Documentation

- [Ports](./ports.md) - Interface that adapters implement
- [Adding Databases](./adding-databases.md) - How to create a new adapter
- [README](./README.md) - Clients layer overview
