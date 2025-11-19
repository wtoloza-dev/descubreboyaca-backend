# Adding New Database Support

This guide walks you through adding support for a new database to the clients layer using the Hexagonal Architecture pattern.

## Overview

To add a new database (e.g., MySQL, MongoDB), you need to:

1. Create an adapter that implements the port
2. Add a dependency factory
3. Configure settings
4. Write tests

The port interface remains unchanged - you're just adding a new implementation.

## Step-by-Step: Adding MySQL Support

Let's add MySQL as an example.

### Step 1: Create Adapter File

Create the adapter file structure:

```bash
mkdir -p app/clients/sql/adapters/mysql
touch app/clients/sql/adapters/mysql/__init__.py
touch app/clients/sql/adapters/mysql/asynchronous.py
```

### Step 2: Implement the Port

```python
# app/clients/sql/adapters/mysql/asynchronous.py

"""MySQL adapter for async SQL operations."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.clients.sql.ports.asynchronous import AsyncSQLClientPort


class AsyncMySQLAdapter:
    """MySQL adapter implementing AsyncSQLClientPort.

    Uses aiomysql driver for asynchronous MySQL operations.

    Attributes:
        database_url: MySQL connection string
        echo: Whether to log SQL queries
        engine: SQLAlchemy async engine
    """

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
    ) -> None:
        """Initialize MySQL adapter.

        Args:
            database_url: MySQL connection URL
                Format: mysql+aiomysql://user:pass@host:port/dbname
            echo: Enable SQL query logging
        """
        self.database_url = database_url
        self.echo = echo
        self.engine: AsyncEngine | None = None

    def connect(self) -> None:
        """Create MySQL engine with connection pooling.

        Configuration:
            - aiomysql driver for async operations
            - Connection pool with health checks
            - MySQL-specific charset and collation
        """
        self.engine = create_async_engine(
            self.database_url,
            echo=self.echo,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            # MySQL-specific options
            connect_args={
                "charset": "utf8mb4",
                "collation": "utf8mb4_unicode_ci",
            },
        )

    async def disconnect(self) -> None:
        """Dispose MySQL engine and close all connections."""
        if self.engine:
            await self.engine.dispose()
            self.engine = None

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get MySQL session.

        Yields:
            AsyncSession: Database session with automatic transaction management
        """
        if not self.engine:
            raise RuntimeError("Engine not initialized. Call connect() first.")

        async with AsyncSession(
            self.engine,
            expire_on_commit=False,
        ) as session:
            yield session
```

### Step 3: Export from Package

```python
# app/clients/sql/adapters/mysql/__init__.py

"""MySQL adapters."""

from app.clients.sql.adapters.mysql.asynchronous import AsyncMySQLAdapter

__all__ = [
    "AsyncMySQLAdapter",
]
```

### Step 4: Create Dependency Factory

```python
# app/clients/sql/dependencies/mysql.py

"""MySQL dependency factories."""

from app.clients.sql.adapters.mysql import AsyncMySQLAdapter
from app.clients.sql.ports.asynchronous import AsyncSQLClientPort
from app.core.settings import settings


def get_async_mysql_client() -> AsyncSQLClientPort:
    """Factory to create async MySQL client.

    Returns:
        AsyncSQLClientPort: MySQL adapter instance

    Example:
        >>> client = get_async_mysql_client()
        >>> client.connect()
        >>> async with client.get_session() as session:
        ...     # Use session
    """
    return AsyncMySQLAdapter(
        database_url=settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
    )
```

### Step 5: Update Main Factory (Optional)

If you want environment-based selection, update the main factory:

```python
# app/clients/sql/dependencies/factory.py

from app.core.settings import settings
from app.clients.sql.ports.asynchronous import AsyncSQLClientPort
from app.clients.sql.adapters.postgres import AsyncPostgreSQLAdapter
from app.clients.sql.adapters.sqlite import AsyncSQLiteAdapter
from app.clients.sql.adapters.mysql import AsyncMySQLAdapter


def get_async_sql_client() -> AsyncSQLClientPort:
    """Factory to create async SQL client based on environment.

    Returns:
        AsyncSQLClientPort: Database adapter based on settings
    """
    if settings.SCOPE == "local":
        return AsyncSQLiteAdapter(
            database_url=settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
        )
    elif settings.DATABASE_TYPE == "mysql":
        return AsyncMySQLAdapter(
            database_url=settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
        )
    else:
        return AsyncPostgreSQLAdapter(
            database_url=settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
        )
```

### Step 6: Update Settings

Add MySQL-specific configuration:

```python
# app/core/settings/base.py

class Settings(BaseSettings):
    """Base application settings."""

    # Database
    DATABASE_URL: str = Field(...)
    DATABASE_TYPE: str = Field(default="postgresql")  # postgresql, mysql, sqlite
    DATABASE_ECHO: bool = Field(default=False)

    # ... other settings
```

### Step 7: Update Environment Variables

```bash
# .env

# For MySQL
DATABASE_TYPE=mysql
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/descubre_boyaca
```

### Step 8: Install Dependencies

```bash
# Add to pyproject.toml or requirements.txt
aiomysql>=0.2.0
```

```bash
uv pip install aiomysql
```

### Step 9: Write Tests

#### Unit Test

```python
# tests/unit/clients/sql/adapters/test_mysql_adapter.py

"""Unit tests for MySQL adapter."""

import pytest
from app.clients.sql.adapters.mysql import AsyncMySQLAdapter


def test_mysql_adapter_initialization():
    """Test MySQL adapter can be initialized."""
    adapter = AsyncMySQLAdapter(
        database_url="mysql+aiomysql://user:pass@localhost/testdb"
    )

    assert adapter.database_url.startswith("mysql+aiomysql://")
    assert adapter.engine is None  # Not connected yet


def test_mysql_adapter_connect():
    """Test MySQL adapter creates engine on connect."""
    adapter = AsyncMySQLAdapter(
        database_url="mysql+aiomysql://user:pass@localhost/testdb"
    )

    adapter.connect()

    assert adapter.engine is not None


@pytest.mark.asyncio
async def test_mysql_adapter_disconnect():
    """Test MySQL adapter disposes engine on disconnect."""
    adapter = AsyncMySQLAdapter(
        database_url="mysql+aiomysql://user:pass@localhost/testdb"
    )

    adapter.connect()
    await adapter.disconnect()

    assert adapter.engine is None
```

#### Integration Test

```python
# tests/integration/clients/sql/adapters/test_mysql_integration.py

"""Integration tests for MySQL adapter."""

import pytest
from sqlmodel import select
from app.clients.sql.adapters.mysql import AsyncMySQLAdapter


@pytest.fixture
async def mysql_adapter(mysql_test_url):
    """Create MySQL adapter for integration testing.

    Args:
        mysql_test_url: Test database URL from fixture
    """
    adapter = AsyncMySQLAdapter(mysql_test_url)
    adapter.connect()
    yield adapter
    await adapter.disconnect()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mysql_adapter_provides_session(mysql_adapter):
    """Test MySQL adapter provides working session."""
    async with mysql_adapter.get_session() as session:
        assert session is not None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mysql_adapter_executes_queries(mysql_adapter):
    """Test queries can be executed through MySQL adapter."""
    async with mysql_adapter.get_session() as session:
        result = await session.execute(select(1))
        assert result.scalar() == 1


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mysql_adapter_connection_info(mysql_adapter):
    """Test MySQL connection returns correct version."""
    async with mysql_adapter.get_session() as session:
        result = await session.execute("SELECT VERSION()")
        version = result.scalar()
        assert "mysql" in version.lower() or "mariadb" in version.lower()
```

### Step 10: Document

Update documentation:

```python
# app/clients/sql/adapters/mysql/__init__.py

"""MySQL database adapter.

This module provides async MySQL adapter implementing the AsyncSQLClientPort.

Supported Versions:
    - MySQL 8.0+
    - MariaDB 10.5+

Driver:
    - aiomysql (async MySQL driver)

Connection URL Format:
    mysql+aiomysql://user:password@host:port/database

Features:
    - Async/await support
    - Connection pooling
    - UTF-8 support (utf8mb4)
    - Automatic reconnection

Example:
    >>> adapter = AsyncMySQLAdapter("mysql+aiomysql://root:pass@localhost/db")
    >>> adapter.connect()
    >>> async with adapter.get_session() as session:
    ...     result = await session.execute(query)
"""
```

## Verification Checklist

Before considering the implementation complete, verify:

- [ ] Adapter implements all methods from `AsyncSQLClientPort`
- [ ] Type hints are correct and match port
- [ ] Docstrings follow Google style
- [ ] `connect()` creates engine successfully
- [ ] `disconnect()` properly disposes resources
- [ ] `get_session()` yields working session
- [ ] Dependency factory returns adapter instance
- [ ] Settings support new database type
- [ ] Unit tests cover adapter methods
- [ ] Integration tests verify database connectivity
- [ ] Documentation is updated
- [ ] Dependencies are added to requirements

## Common Pitfalls

### 1. Forgetting Type Hints

```python
# ❌ Bad - No type hints
def get_session(self):
    async with AsyncSession(self.engine) as session:
        yield session

# ✅ Good - Proper type hints
async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(self.engine) as session:
        yield session
```

### 2. Not Checking Engine Initialization

```python
# ❌ Bad - Can fail if connect() not called
async def get_session(self):
    async with AsyncSession(self.engine) as session:
        yield session

# ✅ Good - Explicit check
async def get_session(self):
    if not self.engine:
        raise RuntimeError("Engine not initialized. Call connect() first.")
    async with AsyncSession(self.engine) as session:
        yield session
```

### 3. Missing Resource Cleanup

```python
# ❌ Bad - Resources not freed
async def disconnect(self):
    pass

# ✅ Good - Proper cleanup
async def disconnect(self):
    if self.engine:
        await self.engine.dispose()
        self.engine = None
```

### 4. Incorrect Connection String Format

```python
# ❌ Bad - Wrong driver
database_url = "mysql://user:pass@host/db"  # Uses mysqlclient (sync)

# ✅ Good - Async driver
database_url = "mysql+aiomysql://user:pass@host/db"  # Uses aiomysql (async)
```

## Testing Strategy

### Unit Tests

Test adapter logic without database:
- Initialization
- Connect/disconnect state management
- Error handling

### Integration Tests

Test with real database:
- Connection establishment
- Query execution
- Transaction management
- Connection pooling

### E2E Tests

Test through application:
- Application startup
- Request handling
- Session management
- Application shutdown

## Related Documentation

- [Ports](./ports.md) - Interface to implement
- [Adapters](./adapters.md) - Existing adapter examples
- [README](./README.md) - Clients layer overview
