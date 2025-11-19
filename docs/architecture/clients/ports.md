# Ports (Interfaces)

## Purpose

Ports are **interfaces** that define the contract all database clients must implement. They specify **what** operations are available without dictating **how** they are implemented.

## Key Concept

In Hexagonal Architecture, ports are the boundaries between your application and the external world. They define the API that adapters must implement.

```
┌─────────────────────────────┐
│     Application Core        │
│  (depends on Port interface)│
└──────────────┬──────────────┘
               │
               │ Port defines contract
               ▼
      ┌────────────────┐
      │  Port Protocol │  ◄── You are here
      └────────────────┘
               │
               │ Adapters implement
               ▼
    ┌──────────┴──────────┐
    │                     │
Adapter A            Adapter B
```

## Implementation: Protocol

Ports use Python's `typing.Protocol` for **structural typing** (duck typing with type checking).

### Why Protocol?

- ✅ No inheritance required - adapters don't need to explicitly inherit
- ✅ Type checkers can verify compliance
- ✅ Flexible - any class with matching methods satisfies the protocol
- ✅ Clear contract definition

## AsyncSQLClientPort

The main port for asynchronous SQL database clients.

### Interface Definition

```python
# app/clients/sql/ports/asynchronous.py

from typing import Protocol, AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession


class AsyncSQLClientPort(Protocol):
    """Port defining the contract for async SQL database clients.

    This protocol must be implemented by all async database adapters
    (PostgreSQL, SQLite, MySQL, etc.). It ensures a consistent interface
    for database operations across different implementations.
    """

    def connect(self) -> None:
        """Establish database connection.

        Should create the database engine and prepare for session creation.
        Called during application startup.

        Example:
            >>> client = AsyncPostgreSQLAdapter(database_url)
            >>> client.connect()
        """
        ...

    async def disconnect(self) -> None:
        """Close database connection and cleanup resources.

        Should dispose of the database engine and clean up any connections.
        Called during application shutdown.

        Example:
            >>> await client.disconnect()
        """
        ...

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an async database session.

        Yields a database session that should be used within an async context.
        The session is automatically managed (commit/rollback).

        Yields:
            AsyncSession: SQLAlchemy async session for database operations

        Example:
            >>> async with client.get_session() as session:
            ...     result = await session.execute(query)
        """
        ...
```

### Method Responsibilities

#### `connect() -> None`

**Purpose**: Initialize the database engine and prepare for connections.

**When Called**: Application startup (in lifespan manager)

**Responsibilities**:
- Create SQLAlchemy engine
- Configure connection pool
- Set up database-specific options (echo, pool size, etc.)

**Example Implementation**:
```python
def connect(self) -> None:
    self.engine = create_async_engine(
        self.database_url,
        echo=self.echo,
        pool_pre_ping=True,
    )
```

#### `disconnect() -> None`

**Purpose**: Clean up database resources and close connections.

**When Called**: Application shutdown (in lifespan manager)

**Responsibilities**:
- Dispose of engine
- Close all connections in pool
- Free resources

**Example Implementation**:
```python
async def disconnect(self) -> None:
    if self.engine:
        await self.engine.dispose()
        self.engine = None
```

#### `get_session() -> AsyncGenerator[AsyncSession, None]`

**Purpose**: Provide a database session for executing queries.

**When Called**: For every request that needs database access

**Responsibilities**:
- Create session from engine
- Yield session to caller
- Automatically commit on success
- Automatically rollback on error
- Close session after use

**Example Implementation**:
```python
async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(self.engine) as session:
        yield session
        # Session automatically closes here
```

## SyncSQLClientPort

The synchronous version for compatibility with sync code.

### Interface Definition

```python
# app/clients/sql/ports/synchronous.py

from typing import Protocol, Generator
from sqlmodel import Session


class SyncSQLClientPort(Protocol):
    """Port defining the contract for sync SQL database clients.

    Similar to AsyncSQLClientPort but for synchronous operations.
    """

    def connect(self) -> None:
        """Establish database connection."""
        ...

    def disconnect(self) -> None:
        """Close database connection."""
        ...

    def get_session(self) -> Generator[Session, None, None]:
        """Get a sync database session.

        Yields:
            Session: SQLAlchemy sync session
        """
        ...
```

## Usage in Application

### In Lifespan Manager

```python
# app/core/lifespan.py

from app.clients.sql.dependencies import get_async_sql_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Get client (could be PostgreSQL or SQLite)
    client: AsyncSQLClientPort = get_async_sql_client()

    # Connect
    client.connect()
    logger.info("Database connected")

    yield

    # Disconnect
    await client.disconnect()
    logger.info("Database disconnected")
```

### In Shared Dependencies

```python
# app/shared/dependencies/sql.py

async def get_async_session_dependency(
    client: Annotated[AsyncSQLClientPort, Depends(get_async_sql_client)],
) -> AsyncGenerator[AsyncSession, None]:
    """Get database session for the request."""
    async with client.get_session() as session:
        yield session
```

### In Repositories

```python
# app/domains/restaurants/infrastructure/persistence/repositories/restaurant/postgresql.py

class PostgreSQLRestaurantRepository:
    def __init__(self, session: AsyncSession) -> None:
        """Initialize with session from port."""
        self.session = session

    async def create(self, data: RestaurantData) -> Restaurant:
        """Use session to persist data."""
        model = RestaurantModel(**data.model_dump())
        self.session.add(model)
        await self.session.commit()
        return self._to_entity(model)
```

## Testing with Ports

### Mock Port Implementation

```python
# tests/mocks/sql_client.py

class MockAsyncSQLClient:
    """Mock implementation of AsyncSQLClientPort for testing."""

    def __init__(self):
        self.connected = False

    def connect(self) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.connected = False

    async def get_session(self) -> AsyncGenerator[MockSession, None]:
        yield MockSession()
```

### Using Mock in Tests

```python
# tests/domains/restaurants/test_repository.py

@pytest.fixture
def mock_client():
    return MockAsyncSQLClient()

async def test_repository_with_mock(mock_client):
    """Test repository with mock client."""
    async with mock_client.get_session() as session:
        repository = RestaurantRepository(session)
        # Test repository operations
```

## Key Principles

1. **Contract Definition** - Port defines WHAT, not HOW
2. **Structural Typing** - Protocol allows duck typing with type safety
3. **No Implementation** - Methods have `...` body, adapters provide implementation
4. **Consistent Interface** - All adapters expose the same API
5. **Testability** - Easy to create mock implementations

## Benefits

| Benefit | Description |
|---------|-------------|
| **Type Safety** | Type checkers verify adapter compliance |
| **Flexibility** | No inheritance required |
| **Clarity** | Contract is explicit and documented |
| **Testability** | Easy to mock for unit tests |
| **IDE Support** | Autocomplete and type hints work perfectly |

## Related Documentation

- [Adapters](./adapters.md) - How ports are implemented for specific databases
- [Adding Databases](./adding-databases.md) - How to implement a port for a new database
- [README](./README.md) - Clients layer overview
