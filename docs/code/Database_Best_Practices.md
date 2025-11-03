# Database Best Practices - SQLModel + FastAPI

This document outlines the best practices for implementing database clients with SQLModel and FastAPI, following SQLAlchemy 2.0 patterns and community recommendations.

## Overview

The implementation follows these key principles:

1. **Hexagonal Architecture** - Ports and Adapters pattern for clean separation
2. **SQLAlchemy 2.0** - Modern async/await patterns and connection pooling
3. **FastAPI Lifespan Events** - Proper resource lifecycle management
4. **Dependency Injection** - Per-request sessions with automatic cleanup

## Architecture

### 1. Ports (Interfaces)

Ports define the contract for database operations without implementation details.

**Location:** `app/clients/sql/ports/`

```python
# SQLClientPort (Synchronous)
class SQLClientPort(Protocol):
    def get_session(self) -> Generator[Session]:
        """Get a database session context manager."""
        ...

# AsyncSQLClientPort (Asynchronous)  
class AsyncSQLClientPort(Protocol):
    async def get_session(self) -> AsyncSession:
        """Get an async database session context manager."""
        ...
```

**Key Points:**
- No `close()` method - lifecycle managed by lifespan events
- Only session management responsibility
- Separate sync/async protocols

### 2. Adapters (Implementations)

Adapters provide concrete implementations for different databases.

**Location:** `app/clients/sql/adapters/`

```python
# SQLite Async Adapter
class SQLiteAsynchronousAdapter:
    def __init__(self, database_url: str, echo: bool = False):
        self.engine = create_async_engine(database_url, echo=echo)
        self.async_session = async_sessionmaker(self.engine, ...)
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.async_session() as session:
            yield session
```

**Key Points:**
- Engine created once in `__init__`
- No `close()` method - engines dispose via lifespan
- Connection pooling managed by SQLAlchemy
- Context managers ensure proper cleanup

### 3. Lifespan Management

FastAPI's lifespan events manage the complete lifecycle of database resources.

**Location:** `app/core/lifespan.py`

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    # Startup: Initialize adapters
    global _sync_adapter, _async_adapter
    _sync_adapter = create_sqlite_adapter(...)
    _async_adapter = create_async_sqlite_adapter(...)
    
    yield  # Application runs
    
    # Shutdown: Dispose engines
    _sync_adapter.engine.dispose()
    await _async_adapter.engine.dispose()
```

**Integration:**

```python
# app/main.py
from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
```

**Benefits:**
- Single adapter instance per application
- Automatic resource cleanup on shutdown
- Connection pool reuse across requests
- Proper error handling

### 4. Dependency Injection

Dependencies provide per-request sessions from the shared adapter.

**Location:** `app/shared/dependencies/sql.py`

```python
async def get_async_session_dependency() -> AsyncGenerator[AsyncSession]:
    """Get async session from shared adapter."""
    adapter = get_async_adapter()  # From lifespan
    async with adapter.get_session() as session:
        yield session
```

**Usage in Routes:**

```python
@router.get("/restaurants")
async def get_restaurants(
    session: AsyncSession = Depends(get_async_session_dependency)
):
    result = await session.exec(select(Restaurant))
    return result.all()
```

**Key Points:**
- Sessions created per-request
- Automatic commit/rollback handling
- Connection returned to pool after request
- No manual cleanup needed

## Best Practices Summary

### ✅ DO

1. **Use lifespan events** for engine initialization and disposal
2. **Create one adapter per application** - reuse across requests
3. **Use dependency injection** for session management
4. **Separate sync and async** - different engines and adapters
5. **Use context managers** for sessions (automatic cleanup)
6. **Configure connection pooling** in engine creation
7. **Keep sessions short-lived** (per-request lifecycle)

### ❌ DON'T

1. **Don't create engines per-request** - use shared adapters
2. **Don't manually close engines** - let lifespan handle it
3. **Don't mix sync and async** - keep them completely separate
4. **Don't keep sessions open** beyond request scope
5. **Don't manage connections manually** - let SQLAlchemy pool handle it
6. **Don't use global sessions** - always use dependency injection

## Configuration

Database settings are centralized in settings:

```python
# app/core/settings/base.py
class BaseAppSettings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./local.db"
    DATABASE_ASYNC_URL: str = "sqlite+aiosqlite:///./local.db"
    DATABASE_ECHO: bool = False
```

Environment-specific overrides:

```python
# app/core/settings/prod.py
class ProdSettings(BaseAppSettings):
    DATABASE_URL: str = "postgresql://..."
    DATABASE_ASYNC_URL: str = "postgresql+asyncpg://..."
    DATABASE_ECHO: bool = False
```

## Migration from Old Pattern

### Before (Anti-pattern)

```python
# ❌ Creating adapter per request
async def get_session():
    adapter = SQLiteAsynchronousAdapter("sqlite+aiosqlite:///./db.db")
    async with adapter.get_session() as session:
        yield session
    await adapter.close()  # Manual cleanup
```

### After (Best Practice)

```python
# ✅ Using shared adapter from lifespan
async def get_session():
    adapter = get_async_adapter()  # Shared instance
    async with adapter.get_session() as session:
        yield session
    # No manual cleanup needed
```

## Connection Pooling

SQLAlchemy automatically manages connection pooling:

```python
# For PostgreSQL (recommended settings)
engine = create_async_engine(
    url,
    pool_pre_ping=True,      # Verify connections before using
    pool_size=5,             # Default pool size
    max_overflow=10,         # Extra connections when needed
)
```

## Testing

For tests, create separate adapter instances:

```python
@pytest.fixture
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def test_session(test_engine):
    async with AsyncSession(test_engine) as session:
        yield session
```

## Performance Benefits

1. **Connection Reuse**: Pool maintains warm connections
2. **Reduced Overhead**: Single engine creation on startup
3. **Better Concurrency**: Async operations don't block
4. **Resource Efficiency**: Automatic connection management

## References

- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Connection Pooling Best Practices](https://docs.sqlalchemy.org/en/20/core/pooling.html)

## Summary

The implementation follows modern Python and FastAPI best practices:

1. ✅ No `close()` methods in ports or adapters
2. ✅ Lifespan events manage engine lifecycle
3. ✅ Shared adapter instances across requests
4. ✅ Per-request sessions via dependency injection
5. ✅ Automatic connection pooling and cleanup
6. ✅ Separate sync/async implementations
7. ✅ Context managers for proper resource management

This approach provides optimal performance, maintainability, and follows community-recommended patterns.

