# Application Lifespan

## Purpose

The lifespan manager handles **application startup and shutdown events**, ensuring proper initialization and cleanup of resources like database connections, caches, and external services.

## Key Concept

**Resource Management**: Initialize resources when the application starts, clean them up when it shuts down.

```
Application Startup
    │
    ├─ Connect to database
    ├─ Initialize cache
    ├─ Set up logging
    └─ Register health checks
    │
    ▼
Application Running (Serving Requests)
    │
    ▼
Application Shutdown
    │
    ├─ Close database connections
    ├─ Flush cache
    ├─ Close external connections
    └─ Clean up resources
```

## Implementation

### Lifespan Context Manager

FastAPI uses an async context manager for lifecycle management:

```python
# app/core/lifespan.py

"""Application lifespan management.

Handles startup and shutdown events for the FastAPI application,
including database connections and resource cleanup.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.clients.sql.dependencies import get_async_sql_client
from app.core.settings import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan.

    Handles startup and shutdown events for database connections,
    logging initialization, and other resources.

    Args:
        app: FastAPI application instance

    Yields:
        None: Control returns to FastAPI for request handling

    Example:
        >>> app = FastAPI(lifespan=lifespan)
        >>> # Application starts
        >>> # Logs: "Database connected"
        >>> # ... serves requests ...
        >>> # Application shuts down
        >>> # Logs: "Database disconnected"
    """
    # ========== STARTUP ==========
    logger.info("=" * 50)
    logger.info("Application startup initiated")
    logger.info(f"Environment: {settings.SCOPE}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info("=" * 50)

    # Initialize database client
    sql_client = get_async_sql_client()

    try:
        # Connect to database
        sql_client.connect()
        logger.info(f"✓ Database connected ({sql_client.__class__.__name__})")

        # Additional startup tasks
        logger.info("✓ Application ready to serve requests")

    except Exception as e:
        logger.error(f"✗ Startup failed: {e}")
        raise

    # ========== YIELD ==========
    # Application is now running and serving requests
    yield

    # ========== SHUTDOWN ==========
    logger.info("=" * 50)
    logger.info("Application shutdown initiated")

    try:
        # Disconnect from database
        await sql_client.disconnect()
        logger.info("✓ Database disconnected")

        # Additional cleanup tasks
        logger.info("✓ Cleanup complete")

    except Exception as e:
        logger.error(f"✗ Shutdown error: {e}")

    logger.info("Application shutdown complete")
    logger.info("=" * 50)
```

### Using Lifespan in Application

```python
# app/main.py

from fastapi import FastAPI
from app.core.lifespan import lifespan

app = FastAPI(
    title="Descubre Boyacá API",
    version="1.0.0",
    lifespan=lifespan,  # Register lifespan manager
)
```

## Startup Tasks

Tasks performed when application starts:

### 1. Database Connection

```python
# Get appropriate database client (PostgreSQL or SQLite)
sql_client = get_async_sql_client()

# Establish connection
sql_client.connect()
logger.info("Database connected")
```

### 2. Logging Configuration

```python
# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger.info("Logging configured")
```

### 3. Environment Information

```python
# Log environment details
logger.info(f"Environment: {settings.SCOPE}")
logger.info(f"Debug mode: {settings.DEBUG}")
logger.info(f"Database: {settings.DATABASE_URL}")
```

### 4. Health Checks (Optional)

```python
# Verify database is accessible
try:
    async with sql_client.get_session() as session:
        await session.execute("SELECT 1")
    logger.info("✓ Database health check passed")
except Exception as e:
    logger.error(f"✗ Database health check failed: {e}")
    raise
```

## Shutdown Tasks

Tasks performed when application shuts down:

### 1. Database Disconnection

```python
# Close database connections
await sql_client.disconnect()
logger.info("Database disconnected")
```

### 2. Resource Cleanup

```python
# Close any open connections
# Flush caches
# Stop background tasks
logger.info("Resources cleaned up")
```

### 3. Graceful Shutdown

```python
# Allow in-flight requests to complete
# Don't accept new requests
# Clean up gracefully
```

## Error Handling

### Startup Failures

```python
try:
    sql_client.connect()
    logger.info("Database connected")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    # Re-raise to prevent application from starting
    raise
```

If startup fails:
- Application won't start
- Error logged
- Process exits with error code

### Shutdown Errors

```python
try:
    await sql_client.disconnect()
    logger.info("Database disconnected")
except Exception as e:
    # Log but don't raise - allow shutdown to continue
    logger.error(f"Error during shutdown: {e}")
```

If shutdown fails:
- Log error
- Continue with other cleanup tasks
- Don't block shutdown process

## Logging Output

### Successful Startup

```
==================================================
Application startup initiated
Environment: local
Debug mode: True
==================================================
✓ Database connected (AsyncSQLiteAdapter)
✓ Application ready to serve requests
```

### Successful Shutdown

```
==================================================
Application shutdown initiated
✓ Database disconnected
✓ Cleanup complete
Application shutdown complete
==================================================
```

### Startup Failure

```
==================================================
Application startup initiated
Environment: prod
Debug mode: False
==================================================
✗ Startup failed: Connection refused
```

## Advanced Usage

### Multiple Resources

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage multiple resources."""

    # Initialize all resources
    sql_client = get_async_sql_client()
    redis_client = get_redis_client()
    s3_client = get_s3_client()

    # Startup
    sql_client.connect()
    await redis_client.connect()
    await s3_client.initialize()

    logger.info("All resources initialized")

    yield

    # Shutdown
    await sql_client.disconnect()
    await redis_client.disconnect()
    await s3_client.cleanup()

    logger.info("All resources cleaned up")
```

### Background Tasks

```python
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Start background tasks."""

    # Start background tasks
    cleanup_task = asyncio.create_task(periodic_cleanup())
    health_check_task = asyncio.create_task(health_monitor())

    logger.info("Background tasks started")

    yield

    # Cancel background tasks
    cleanup_task.cancel()
    health_check_task.cancel()

    # Wait for cancellation
    await asyncio.gather(cleanup_task, health_check_task, return_exceptions=True)

    logger.info("Background tasks stopped")
```

### Database Migrations

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Run database migrations on startup."""

    sql_client = get_async_sql_client()
    sql_client.connect()

    # Run migrations
    if settings.RUN_MIGRATIONS:
        logger.info("Running database migrations...")
        await run_migrations()
        logger.info("✓ Migrations complete")

    yield

    await sql_client.disconnect()
```

## Testing

### Test Startup

```python
import pytest
from app.core.lifespan import lifespan


@pytest.mark.asyncio
async def test_lifespan_startup(app):
    """Test application startup is successful."""
    async with lifespan(app):
        # Application is running
        # Database should be connected
        from app.clients.sql.dependencies import get_async_sql_client

        client = get_async_sql_client()
        assert client.engine is not None
```

### Test Shutdown

```python
@pytest.mark.asyncio
async def test_lifespan_shutdown(app):
    """Test application shutdown is clean."""
    async with lifespan(app):
        pass  # Enter and exit context

    # After exit, database should be disconnected
    from app.clients.sql.dependencies import get_async_sql_client

    client = get_async_sql_client()
    # Verify cleanup occurred
```

### Mock Lifespan in Tests

```python
@pytest.fixture
async def app():
    """Create test application without lifespan."""
    from fastapi import FastAPI

    # Create app without lifespan for testing
    app = FastAPI()

    # Manually set up test resources
    yield app

    # Manually tear down test resources
```

## Best Practices

### 1. Log Important Events

```python
# ✅ Good - Clear logging
logger.info("✓ Database connected")
logger.error("✗ Connection failed")

# ❌ Bad - No logging
sql_client.connect()
```

### 2. Handle Errors Gracefully

```python
# ✅ Good - Try/except with logging
try:
    sql_client.connect()
except Exception as e:
    logger.error(f"Connection failed: {e}")
    raise

# ❌ Bad - Unhandled exceptions
sql_client.connect()  # Could crash without logging
```

### 3. Fail Fast on Startup

```python
# ✅ Good - Raise on critical startup failures
if not critical_resource_available():
    raise RuntimeError("Cannot start without critical resource")

# ❌ Bad - Continue with degraded state
if not critical_resource_available():
    logger.warning("Resource unavailable, continuing anyway")
```

### 4. Don't Block Shutdown

```python
# ✅ Good - Log errors but continue shutdown
try:
    await cleanup_resource()
except Exception as e:
    logger.error(f"Cleanup error: {e}")  # Log and continue

# ❌ Bad - Raise during shutdown
await cleanup_resource()  # Could block shutdown
```

## Related Documentation

- [README](./README.md) - Core layer overview
- [Settings](./settings.md) - Configuration used in lifespan
- [Clients Layer](../clients/README.md) - Database client initialization
- [ARCHITECTURE.md - Section 6.4](../../../ARCHITECTURE.md#64-application-lifespan)
