# Dependencies (Dependency Injection)

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Dependencies** | `Infrastructure Layer` | `DDD` `Dependency Injection` `FastAPI DI` `IoC` |

## Definition

Dependencies are FastAPI dependency injection functions that provide instances of services, repositories, and utilities to route handlers. They implement the Dependency Injection (DI) pattern, enabling loose coupling, testability, and separation of concerns by delegating the creation and management of dependencies to the framework.

**Key Characteristics:**
- **Dependency Injection**: Automatically inject dependencies into route handlers
- **Lazy Evaluation**: Dependencies are resolved only when needed
- **Hierarchical Dependencies**: Dependencies can depend on other dependencies
- **Type Safety**: Full type hint support for IDE and static analysis
- **Testability**: Easy to override dependencies for testing
- **Singleton/Factory Pattern**: Control instance creation lifecycle
- **Interface-Based**: Depend on abstractions, not concrete implementations

## Architecture Pattern

```
┌────────────────────────────────────────────────────────────┐
│                     Route Handler                          │
│                 (Presentation Layer)                       │
└──────────────────────────┬─────────────────────────────────┘
                           │ requests
                           ↓
┌────────────────────────────────────────────────────────────┐
│              FastAPI Dependency Injection                  │
│                  (Framework Layer)                         │
│   ┌────────────────────────────────────────────────┐       │
│   │   Resolves dependencies automatically          │       │
│   │   - Analyzes function signatures               │       │
│   │   - Calls dependency providers                 │       │
│   │   - Injects resolved instances                 │       │
│   └────────────────────────────────────────────────┘       │
└──────────────────────────┬─────────────────────────────────┘
                           │ calls
                           ↓
┌────────────────────────────────────────────────────────────┐
│              Dependency Functions                          │
│                (dependencies/ modules)                     │
│   ┌────────────────────────────────────────────────┐       │
│   │  Service Dependencies                          │       │
│   │  └─→ get_xxx_service_dependency()              │       │
│   │       └─→ Injects repositories                 │       │
│   │            └─→ Returns service instance        │       │
│   │                                                │       │
│   │  Repository Dependencies                       │       │
│   │  └─→ get_xxx_repository_dependency()           │       │
│   │       └─→ Injects database session             │       │
│   │            └─→ Returns repository instance     │       │
│   │                                                │       │
│   │  Shared Dependencies                           │       │
│   │  └─→ get_pagination_dependency()               │       │
│   │  └─→ get_request_by_dependency()               │       │
│   │  └─→ get_async_sql_session_dependency()        │       │
│   └────────────────────────────────────────────────┘       │
└──────────────────────────┬─────────────────────────────────┘
                           │ creates/returns
                           ↓
┌────────────────────────────────────────────────────────────┐
│          Concrete Instances (Services/Repos)               │
│                                                            │
│   Services → Repositories → Database/HTTP Clients          │
└────────────────────────────────────────────────────────────┘
```

**Dependency Resolution Flow:**
1. **Route Handler** declares dependencies via `Depends()`
2. **FastAPI DI** analyzes function signatures recursively
3. **Dependency Functions** are called in the correct order
4. **Nested Dependencies** are resolved automatically
5. **Instances** are injected into the route handler
6. **Route Handler** executes with all dependencies available

## File & Naming Rules

### Directory Structure

| Element | Rule | Example |
|---------|------|---------|
| **Domain Dependencies** | `app/domains/{domain}/dependencies/` | `app/domains/prompt/dependencies/` |
| **Shared Dependencies** | `app/shared/dependencies/` | `app/shared/dependencies/pagination.py` |
| **Client Dependencies** | `app/clients/{client}/dependencies/` | `app/clients/http/dependencies/` |

### File Naming

| Pattern | Rule | Example | ❌ Avoid |
|---------|------|---------|----------|
| **Resource Dependencies** | `{resource}_snake_case.py` | `prompt.py`, `prompt_version.py` | `prompt_deps.py`, `prompt_di.py` |
| **Shared Utilities** | `{utility}.py` | `pagination.py`, `request_by.py`, `sql.py` | `utils.py`, `helpers.py` |
| **Package Init** | `__init__.py` | Exports all dependency functions | N/A |

### Function Naming

| Pattern | Rule | Example | ❌ Avoid |
|---------|------|---------|----------|
| **Service Dependencies** | `get_{resource}_service_dependency` | `get_prompt_service_dependency()` | `prompt_service()`, `provide_service()` |
| **Repository Dependencies** | `get_{resource}_repository_dependency` | `get_prompt_repository_dependency()` | `create_repository()`, `repo()` |
| **Utility Dependencies** | `get_{utility}_dependency` | `get_pagination_dependency()` | `pagination()`, `get_pagination()` |

**Naming Convention:**
```
get_{resource}_{type}_dependency()
    ↓         ↓        ↓
  action   name    category

Examples:
- get_prompt_service_dependency()
- get_prompt_version_repository_dependency()
- get_pagination_dependency()
- get_request_by_dependency()
```

## Implementation Rules

### Basic Dependency Structure

```python
"""[Resource] dependencies for FastAPI dependency injection."""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.xxx.domain.interfaces import XxxRepositoryInterface
from app.domains.xxx.repositories import MySQLXxxRepository
from app.domains.xxx.services import XxxService
from app.shared.dependencies.sql import get_async_sql_session_dependency


def get_xxx_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_sql_session_dependency)],
) -> XxxRepositoryInterface:
    """Get xxx repository.
    
    Args:
        session: Async database session dependency.
    
    Returns:
        XxxRepositoryInterface: Repository instance.
    """
    return MySQLXxxRepository(session=session)


def get_xxx_service_dependency(
    repository: Annotated[
        XxxRepositoryInterface, Depends(get_xxx_repository_dependency)
    ],
) -> XxxService:
    """Get xxx service.
    
    Args:
        repository: Repository implementation.
    
    Returns:
        XxxService: Service instance with injected dependencies.
    """
    return XxxService(repository=repository)
```

**Key Points:**
- ✅ Use `Annotated` with `Depends()` for all nested dependencies
- ✅ Return interface types (e.g., `XxxRepositoryInterface`)
- ✅ Create and return concrete implementations
- ✅ Include comprehensive docstrings
- ✅ Chain dependencies hierarchically

### Dependency Type Annotations

```python
from typing import Annotated
from fastapi import Depends

# ✅ CORRECT - Annotated with Depends
def get_service_dependency(
    repository: Annotated[
        PromptRepositoryInterface, 
        Depends(get_prompt_repository_dependency)
    ],
) -> PromptService:
    """Properly annotated dependency."""
    return PromptService(repository=repository)

# ❌ INCORRECT - Missing Annotated
def get_service_dependency(
    repository: PromptRepositoryInterface = Depends(get_prompt_repository_dependency),
) -> PromptService:
    """Old-style annotation (pre-Python 3.9)."""
    return PromptService(repository=repository)
```

## Dependency Patterns

### Pattern 1: Repository Dependency (Database)

Repository dependencies inject database sessions and return repository instances.

```python
"""Prompt repository dependency."""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.domains.prompt.domain.interfaces import PromptRepositoryInterface
from app.domains.prompt.repositories import (
    MySQLPromptRepository,
    SQLitePromptRepository,
)
from app.shared.dependencies.sql import get_async_sql_session_dependency


def get_prompt_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_sql_session_dependency)],
) -> PromptRepositoryInterface:
    """Get prompt repository based on environment.
    
    This function returns the appropriate repository implementation
    based on the application scope (local vs production).
    
    Args:
        session: Async database session dependency.
    
    Returns:
        PromptRepositoryInterface: Repository instance (MySQL or SQLite).
    """
    if settings.SCOPE == "local":
        return SQLitePromptRepository(session=session)
    return MySQLPromptRepository(session=session)
```

**Key Points:**
- ✅ Injects database session via `get_async_sql_session_dependency`
- ✅ Returns interface type (`PromptRepositoryInterface`)
- ✅ Environment-based implementation selection
- ✅ Creates concrete repository instances

### Pattern 2: Service Dependency (Single Repository)

Service dependencies inject repositories and return service instances.

```python
"""Prompt history service dependency."""

from typing import Annotated

from fastapi import Depends

from app.domains.prompt.domain.interfaces import PromptHistoryRepositoryInterface
from app.domains.prompt.services import PromptHistoryService

from .prompt_history import get_prompt_history_repository_dependency


def get_prompt_history_service_dependency(
    repository: Annotated[
        PromptHistoryRepositoryInterface,
        Depends(get_prompt_history_repository_dependency),
    ],
) -> PromptHistoryService:
    """Get prompt history service.
    
    Args:
        repository: Prompt history repository implementation.
    
    Returns:
        PromptHistoryService: Service instance with injected dependencies.
    """
    return PromptHistoryService(repository=repository)
```

**Key Points:**
- ✅ Injects repository via `Depends()`
- ✅ Returns concrete service instance
- ✅ Uses interface type for repository parameter
- ✅ Single responsibility (one repository)

### Pattern 3: Service Dependency (Multiple Repositories)

Complex services may require multiple repository dependencies.

```python
"""Prompt service dependency."""

from typing import Annotated

from fastapi import Depends

from app.domains.prompt.domain.interfaces import (
    PromptOwnershipRepositoryInterface,
    PromptRepositoryInterface,
)
from app.domains.prompt.services import PromptService

from .prompt import get_prompt_repository_dependency
from .prompt_ownership import get_prompt_ownership_repository_dependency


def get_prompt_service_dependency(
    repository: Annotated[
        PromptRepositoryInterface, Depends(get_prompt_repository_dependency)
    ],
    ownership_repository: Annotated[
        PromptOwnershipRepositoryInterface,
        Depends(get_prompt_ownership_repository_dependency),
    ],
) -> PromptService:
    """Get prompt service with repositories.
    
    This service requires both the main prompt repository and the
    ownership repository to manage prompt access control.
    
    Args:
        repository: Prompt repository implementation.
        ownership_repository: Ownership repository implementation.
    
    Returns:
        PromptService: Service instance with all injected dependencies.
    """
    return PromptService(
        repository=repository, 
        ownership_repository=ownership_repository
    )
```

**Key Points:**
- ✅ Multiple repository dependencies
- ✅ Each dependency injected via `Depends()`
- ✅ Clear parameter naming
- ✅ All dependencies passed to service constructor

### Pattern 4: Service Dependency (Orchestrator/Coordinator)

Orchestrator services coordinate multiple domain services or repositories.

```python
"""Publish service dependency."""

from typing import Annotated

from fastapi import Depends

from app.domains.prompt.domain.interfaces import (
    PromptHistoryRepositoryInterface,
    PromptRepositoryInterface,
    PromptVersionRepositoryInterface,
)
from app.domains.prompt.services import PublishService

from .prompt import get_prompt_repository_dependency
from .prompt_history import get_prompt_history_repository_dependency
from .prompt_version import get_prompt_version_repository_dependency


def get_publish_service_dependency(
    prompt_repository: Annotated[
        PromptRepositoryInterface, Depends(get_prompt_repository_dependency)
    ],
    prompt_version_repository: Annotated[
        PromptVersionRepositoryInterface,
        Depends(get_prompt_version_repository_dependency),
    ],
    prompt_history_repository: Annotated[
        PromptHistoryRepositoryInterface,
        Depends(get_prompt_history_repository_dependency),
    ],
) -> PublishService:
    """Get publish service dependency.
    
    The publish service orchestrates the promotion of prompt versions
    to production by coordinating across prompt, version, and history
    repositories.
    
    Args:
        prompt_repository: Injected prompt repository.
        prompt_version_repository: Injected prompt version repository.
        prompt_history_repository: Injected prompt history repository.
    
    Returns:
        PublishService: Configured publish service instance.
    """
    return PublishService(
        prompt_repository=prompt_repository,
        prompt_version_repository=prompt_version_repository,
        prompt_history_repository=prompt_history_repository,
    )
```

**Key Points:**
- ✅ Orchestrates multiple repositories
- ✅ Complex business operations across domains
- ✅ All dependencies explicitly injected
- ✅ Clear documentation of orchestration purpose

### Pattern 5: Service Dependency (Inline Repository Creation)

Sometimes services create repositories inline instead of using separate dependency functions.

```python
"""Prompt version service dependency."""

from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.prompt.domain.interfaces import (
    PromptRepositoryInterface,
    PromptVersionRepositoryInterface,
)
from app.domains.prompt.repositories import (
    MySQLPromptRepository,
    MySQLPromptVersionRepository,
)
from app.domains.prompt.services import PromptVersionService
from app.shared.dependencies.sql import get_async_sql_session_dependency


def get_prompt_version_service_dependency(
    session: Annotated[AsyncSession, Depends(get_async_sql_session_dependency)],
) -> PromptVersionService:
    """Get prompt version service.
    
    This dependency creates repository instances inline instead of
    using separate repository dependency functions.
    
    Args:
        session: Async database session dependency.
    
    Returns:
        PromptVersionService: Service instance with repository dependencies.
    """
    repository: PromptVersionRepositoryInterface = MySQLPromptVersionRepository(
        session=session
    )
    prompt_repository: PromptRepositoryInterface = MySQLPromptRepository(
        session=session
    )
    
    return PromptVersionService(
        repository=repository, 
        prompt_repository=prompt_repository
    )
```

**Key Points:**
- ✅ Injects session directly
- ✅ Creates repositories inline
- ✅ Type annotations for clarity
- ✅ Useful when repositories aren't needed elsewhere
- ⚠️ Use sparingly - prefer separate repository dependencies for reusability

### Pattern 6: API Client Dependency

Dependencies for external API clients (HTTP, gRPC, etc.).

```python
"""GenAI service dependency."""

from typing import Annotated

from fastapi import Depends

from app.clients.http import HTTPClientMeliTK, get_http_client_melitk_dependency
from app.domains.genai.domain.interfaces import GenAIAPIRepositoryInterface
from app.domains.genai.repositories import RESTGenAIAPIRepository
from app.domains.genai.services import GenaiService


def get_genai_service_dependency(
    http_client: Annotated[
        HTTPClientMeliTK, Depends(get_http_client_melitk_dependency)
    ],
) -> GenaiService:
    """Get GenAI service dependency.
    
    This function constructs and returns a configured GenAI service instance
    with all necessary dependencies injected for external API communication.
    
    Args:
        http_client: HTTP client for external API calls (injected dependency).
    
    Returns:
        GenaiService: Configured GenAI service instance.
    """
    repository: GenAIAPIRepositoryInterface = RESTGenAIAPIRepository(
        http_client=http_client
    )
    return GenaiService(repository=repository)
```

**Key Points:**
- ✅ Injects HTTP client instead of database session
- ✅ Creates API repository (REST, gRPC, etc.)
- ✅ Same pattern as database dependencies
- ✅ Infrastructure abstraction maintained

### Pattern 7: Shared Utility Dependencies

Shared dependencies for common utilities like pagination, authentication, etc.

#### Pagination Dependency

```python
"""FastAPI dependency for pagination query parameters."""

from fastapi import Query

from app.shared.domain.value_objects.pagination import Pagination


def get_pagination_dependency(
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    size: int = Query(default=10, ge=1, le=20, description="Page size"),
) -> Pagination:
    """Create a Pagination entity from query parameters.
    
    This dependency extracts pagination parameters from the request query string
    and returns a validated Pagination value object.
    
    Args:
        page: The page number to retrieve (1-based indexing, minimum 1).
        size: The number of items per page (minimum 1, maximum 20).
    
    Returns:
        Pagination: Validated pagination value object.
    """
    return Pagination(page=page, size=size)
```

**Key Points:**
- ✅ Uses `Query()` for query parameter validation
- ✅ Default values and constraints
- ✅ Returns domain value object
- ✅ No nested dependencies

#### Request Header Dependency

```python
"""Request by dependency."""

from typing import Annotated

from fastapi import Header


def get_request_by_dependency(x_request_by: Annotated[str, Header()]) -> str:
    """Get request by (user ID) from request headers.
    
    This dependency extracts the user identifier from the
    X-Request-By HTTP header for authentication and audit trails.
    
    Args:
        x_request_by: Request by header value (user identifier).
    
    Returns:
        str: User identifier from header.
    """
    return x_request_by
```

**Key Points:**
- ✅ Uses `Header()` for header extraction
- ✅ FastAPI automatically converts header names (X-Request-By → x_request_by)
- ✅ Returns simple type (string)
- ✅ Used for authentication/audit

#### Database Session Dependency

```python
"""SQL database session dependencies."""

from collections.abc import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from app.clients.sql.dependencies import (
    create_async_mysql_client_dependency,
    create_async_sqlite_client_dependency,
)
from app.clients.sql.ports import AsyncSQLClientPort
from app.core.settings import settings


async def get_async_sql_session_dependency() -> AsyncGenerator[AsyncSession]:
    """Get an asynchronous SQL session dependency.
    
    Constructs the database URI using the appropriate asynchronous driver
    based on the application scope (local vs production).
    
    Yields:
        AsyncSession: Async database session for queries and transactions.
    """
    client: AsyncSQLClientPort
    
    if settings.SCOPE == "local":
        db_uri = f"sqlite+aiosqlite:///{settings.DB_CONNECTION_STRING}"
        client = create_async_sqlite_client_dependency(db_uri)
    else:
        db_uri = f"mysql+aiomysql://{settings.DB_CONNECTION_STRING}"
        client = create_async_mysql_client_dependency(db_uri)
    
    async with client.get_session() as session:
        yield session
```

**Key Points:**
- ✅ Async generator pattern
- ✅ Environment-based database selection
- ✅ Context manager for session lifecycle
- ✅ Automatic session cleanup
- ✅ Shared across all repository dependencies

## Package Organization

### Domain Dependencies Package (`__init__.py`)

```python
"""Prompt dependencies package.

This module exports all dependency injection functions for the prompt domain,
including service and repository dependencies.
"""

from .prompt import get_prompt_service_dependency
from .prompt_history import get_prompt_history_service_dependency
from .prompt_ownership import get_prompt_ownership_repository_dependency
from .prompt_version import get_prompt_version_service_dependency
from .publish import get_publish_service_dependency


__all__ = [
    "get_prompt_service_dependency",
    "get_prompt_version_service_dependency",
    "get_prompt_history_service_dependency",
    "get_publish_service_dependency",
    "get_prompt_ownership_repository_dependency",
]
```

**Key Points:**
- ✅ Module docstring describing purpose
- ✅ Import all dependency functions
- ✅ Export via `__all__`
- ✅ Alphabetically ordered (grouped by type)
- ✅ Clear naming for external usage

### Shared Dependencies Package (`__init__.py`)

```python
"""Shared dependencies package.

This module exports common dependency injection functions used across
multiple domains, including pagination, authentication, and database sessions.
"""

from .pagination import get_pagination_dependency
from .request_by import get_request_by_dependency
from .sql import get_async_sql_session_dependency, get_sql_session_dependency


__all__ = [
    "get_pagination_dependency",
    "get_request_by_dependency",
    "get_async_sql_session_dependency",
    "get_sql_session_dependency",
]
```

## Usage in Routes

### Basic Service Injection

```python
"""Prompt find by ID route."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path
from ulid import ULID

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.schemas import FindByIdPromptSchemaResponse
from app.domains.prompt.services import PromptService


router = APIRouter()


@router.get(path="/{prompt_id}/")
async def handle_find_by_id(
    prompt_id: Annotated[ULID, Path(description="Prompt ID")],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> FindByIdPromptSchemaResponse:
    """Handle find prompt by ID endpoint.
    
    Args:
        prompt_id: Unique identifier of the prompt.
        service: Injected prompt service (via DI).
    
    Returns:
        Complete prompt information.
    """
    prompt = await service.get_by_id(prompt_id=str(prompt_id))
    return FindByIdPromptSchemaResponse.model_validate(prompt)
```

### Multiple Dependencies

```python
"""Prompt create route."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.domain.entities import PromptData
from app.domains.prompt.schemas import (
    CreatePromptSchemaRequest,
    CreatePromptSchemaResponse,
)
from app.domains.prompt.services import PromptService
from app.shared.dependencies import get_request_by_dependency


router = APIRouter()


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def handle_create_prompt(
    request: Annotated[CreatePromptSchemaRequest, Body()],
    current_user: Annotated[str, Depends(get_request_by_dependency)],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> CreatePromptSchemaResponse:
    """Handle create prompt endpoint.
    
    Args:
        request: Prompt creation data.
        current_user: Authenticated user identifier (from header).
        service: Injected prompt service (via DI).
    
    Returns:
        Created prompt with ID and metadata.
    """
    prompt_data = PromptData.model_validate(request)
    prompt = await service.create(prompt_data, current_user)
    return CreatePromptSchemaResponse.model_validate(prompt)
```

### Pagination Dependency

```python
"""Prompt find all route."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.schemas import FindAllPromptSchemaResponse
from app.domains.prompt.services import PromptService
from app.shared.dependencies.pagination import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas.pagination import PaginationSchemaData


router = APIRouter()


@router.get(path="/")
async def handle_find_all(
    pagination_request: Annotated[Pagination, Depends(get_pagination_dependency)],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> FindAllPromptSchemaResponse:
    """Handle find all prompts endpoint.
    
    Args:
        pagination_request: Pagination parameters (page, size).
        service: Injected prompt service (via DI).
    
    Returns:
        Paginated list of all prompts.
    """
    prompts, total = await service.find_all(
        offset=pagination_request.offset,
        limit=pagination_request.limit,
    )
    return FindAllPromptSchemaResponse(
        data=[FindAllPromptSchemaItem.model_validate(p) for p in prompts],
        pagination=PaginationSchemaData(
            total=total,
            total_per_page=pagination_request.size,
            current_page=pagination_request.page,
        ),
    )
```

## Import Patterns

### Standard Dependency Imports

```python
"""[Resource] dependencies for FastAPI dependency injection."""

# Standard library
from typing import Annotated

# FastAPI framework
from fastapi import Depends

# Database clients
from sqlmodel.ext.asyncio.session import AsyncSession

# Application settings
from app.core.settings import settings

# Domain interfaces
from app.domains.xxx.domain.interfaces import (
    XxxRepositoryInterface,
    YyyRepositoryInterface,
)

# Domain repositories
from app.domains.xxx.repositories import (
    MySQLXxxRepository,
    SQLiteXxxRepository,
)

# Domain services
from app.domains.xxx.services import XxxService

# Shared dependencies
from app.shared.dependencies.sql import get_async_sql_session_dependency

# Local dependencies (relative imports for same package)
from .yyy import get_yyy_repository_dependency
```

**Import Order:**
1. Standard library (`typing`)
2. FastAPI framework
3. Database/HTTP clients
4. Application settings
5. Domain interfaces
6. Domain repositories
7. Domain services
8. Shared dependencies
9. Local dependencies (relative imports)

## Best Practices

### ✅ DO

1. **Use `Annotated` with `Depends()`** for all dependencies
2. **Return interface types** when possible (e.g., `XxxRepositoryInterface`)
3. **Name functions consistently** (`get_{resource}_{type}_dependency`)
4. **Include comprehensive docstrings** (Args, Returns, description)
5. **Chain dependencies hierarchically** (session → repository → service)
6. **Use type hints everywhere** for IDE support and type checking
7. **Export all functions in `__init__.py`** for easy imports
8. **Keep dependencies simple** - one clear responsibility per function
9. **Use environment-based selection** when needed (local vs prod)
10. **Document environment differences** in docstrings
11. **Separate concerns** - repository deps separate from service deps
12. **Reuse shared dependencies** (session, pagination, auth)

### ❌ DON'T

1. **Don't instantiate dependencies in routes** - always use `Depends()`
2. **Don't create complex logic in dependency functions** - keep them simple
3. **Don't forget type hints** - all parameters and returns must be typed
4. **Don't use global instances** - dependencies should be factory functions
5. **Don't skip docstrings** - document all dependency functions
6. **Don't mix concerns** - keep infrastructure separate from business logic
7. **Don't hardcode implementations** - use environment-based selection
8. **Don't create circular dependencies** - maintain clear hierarchy
9. **Don't use old-style annotations** (`param: Type = Depends()`)
10. **Don't instantiate services/repositories outside dependencies** - DI only

## Testing Dependencies

### Override Dependencies in Tests

```python
"""Test example with dependency override."""

import pytest
from fastapi.testclient import TestClient

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.services import PromptService
from app.main import app


class MockPromptService(PromptService):
    """Mock service for testing."""
    
    async def get_by_id(self, prompt_id: str):
        """Mock implementation."""
        return MockPrompt(id=prompt_id, name="Test Prompt")


@pytest.fixture
def client_with_mock_service():
    """Create test client with mocked service."""
    
    def mock_get_prompt_service():
        return MockPromptService(repository=None)
    
    # Override dependency
    app.dependency_overrides[get_prompt_service_dependency] = mock_get_prompt_service
    
    with TestClient(app) as client:
        yield client
    
    # Clean up
    app.dependency_overrides.clear()


def test_find_by_id(client_with_mock_service):
    """Test endpoint with mocked service."""
    response = client_with_mock_service.get("/prompt/01234567890123456789012345/")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Prompt"
```

**Key Points:**
- ✅ Use `app.dependency_overrides` to replace dependencies
- ✅ Create mock implementations for testing
- ✅ Clean up overrides after tests
- ✅ Test isolation via dependency injection

## Checklist for New Dependencies

- [ ] **File named semantically** (e.g., `prompt.py`, `prompt_version.py`)
- [ ] **Module docstring** present and descriptive
- [ ] **Function named correctly** (`get_{resource}_{type}_dependency`)
- [ ] **Uses `Annotated` with `Depends()`** for all nested dependencies
- [ ] **Type hints** on all parameters and return types
- [ ] **Returns interface type** (if applicable)
- [ ] **Comprehensive docstring** with Args and Returns
- [ ] **Proper import order** (standard → framework → domain → shared)
- [ ] **Exported in `__init__.py`** of the package
- [ ] **No business logic** - only dependency wiring
- [ ] **Environment-based selection** documented (if applicable)
- [ ] **Reuses shared dependencies** (session, pagination, etc.)
- [ ] **Follows dependency hierarchy** (session → repo → service)
- [ ] **No circular dependencies** - clear dependency graph

## Common Mistakes

### Mistake 1: Old-Style Annotations

```python
# ❌ BAD - Old-style annotation (pre-Python 3.9)
def get_service_dependency(
    repository: PromptRepositoryInterface = Depends(get_repository_dependency),
) -> PromptService:
    pass

# ✅ GOOD - Use Annotated
def get_service_dependency(
    repository: Annotated[
        PromptRepositoryInterface, Depends(get_repository_dependency)
    ],
) -> PromptService:
    pass
```

### Mistake 2: Missing Type Hints

```python
# ❌ BAD - No return type
def get_prompt_service_dependency(repository):
    return PromptService(repository=repository)

# ✅ GOOD - Full type hints
def get_prompt_service_dependency(
    repository: Annotated[
        PromptRepositoryInterface, Depends(get_prompt_repository_dependency)
    ],
) -> PromptService:
    return PromptService(repository=repository)
```

### Mistake 3: Business Logic in Dependencies

```python
# ❌ BAD - Business logic in dependency
def get_prompt_service_dependency(
    session: Annotated[AsyncSession, Depends(get_async_sql_session_dependency)],
) -> PromptService:
    repository = MySQLPromptRepository(session=session)
    
    # ❌ Business logic doesn't belong here
    if repository.count() > 100:
        repository.cleanup()
    
    return PromptService(repository=repository)

# ✅ GOOD - Only dependency wiring
def get_prompt_service_dependency(
    repository: Annotated[
        PromptRepositoryInterface, Depends(get_prompt_repository_dependency)
    ],
) -> PromptService:
    return PromptService(repository=repository)
```

### Mistake 4: Direct Instantiation in Routes

```python
# ❌ BAD - Direct instantiation in route
@router.get("/{prompt_id}/")
async def handle_find_by_id(prompt_id: ULID):
    session = await get_async_sql_session_dependency()  # ❌ Manual call
    repository = MySQLPromptRepository(session=session)
    service = PromptService(repository=repository)
    return await service.get_by_id(prompt_id=str(prompt_id))

# ✅ GOOD - Use dependency injection
@router.get("/{prompt_id}/")
async def handle_find_by_id(
    prompt_id: ULID,
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
):
    return await service.get_by_id(prompt_id=str(prompt_id))
```

### Mistake 5: Returning Concrete Types Instead of Interfaces

```python
# ❌ BAD - Returns concrete type
def get_prompt_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_sql_session_dependency)],
) -> MySQLPromptRepository:  # ❌ Concrete type
    return MySQLPromptRepository(session=session)

# ✅ GOOD - Returns interface type
def get_prompt_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_sql_session_dependency)],
) -> PromptRepositoryInterface:  # ✅ Interface type
    if settings.SCOPE == "local":
        return SQLitePromptRepository(session=session)
    return MySQLPromptRepository(session=session)
```

### Mistake 6: Missing Docstrings

```python
# ❌ BAD - No docstring
def get_prompt_service_dependency(
    repository: Annotated[
        PromptRepositoryInterface, Depends(get_prompt_repository_dependency)
    ],
) -> PromptService:
    return PromptService(repository=repository)

# ✅ GOOD - Comprehensive docstring
def get_prompt_service_dependency(
    repository: Annotated[
        PromptRepositoryInterface, Depends(get_prompt_repository_dependency)
    ],
) -> PromptService:
    """Get prompt service with injected dependencies.
    
    Args:
        repository: Prompt repository implementation.
    
    Returns:
        PromptService: Service instance with repository dependency.
    """
    return PromptService(repository=repository)
```

## Dependency Hierarchy Examples

### Simple Hierarchy (3 Levels)

```
Route Handler
    ↓ injects
Service Dependency
    ↓ injects
Repository Dependency
    ↓ injects
Database Session Dependency
```

**Example:**
```python
# Level 3: Session (shared)
get_async_sql_session_dependency() → AsyncSession

# Level 2: Repository
get_prompt_repository_dependency(session) → PromptRepositoryInterface

# Level 1: Service
get_prompt_service_dependency(repository) → PromptService

# Level 0: Route Handler
handle_find_by_id(service) → Response
```

### Complex Hierarchy (Multi-Repository Service)

```
Route Handler
    ↓ injects
Service Dependency (Multiple repos)
    ↓ injects       ↓ injects       ↓ injects
Repository A    Repository B    Repository C
    ↓ injects       ↓ injects       ↓ injects
      Database Session (shared)
```

**Example:**
```python
# Shared session
get_async_sql_session_dependency() → AsyncSession

# Multiple repositories
get_prompt_repository_dependency(session) → PromptRepositoryInterface
get_prompt_version_repository_dependency(session) → PromptVersionRepositoryInterface
get_prompt_history_repository_dependency(session) → PromptHistoryRepositoryInterface

# Orchestrator service
get_publish_service_dependency(
    prompt_repository,
    prompt_version_repository,
    prompt_history_repository,
) → PublishService

# Route handler
handle_publish(service) → Response
```

---

## Summary

Dependencies are **FastAPI dependency injection functions** that:
- Wire up services, repositories, and utilities
- Enable loose coupling and testability
- Provide interface-based abstractions
- Manage instance lifecycle automatically
- Support hierarchical dependency graphs

**Golden Rules:**
1. ✅ Use **`Annotated` with `Depends()`** for all dependencies
2. ✅ Return **interface types** when possible
3. ✅ Follow **naming convention** (`get_{resource}_{type}_dependency`)
4. ✅ Keep dependencies **simple** - only wiring, no business logic
5. ✅ Use **comprehensive docstrings** (Args, Returns, description)
6. ✅ Maintain **clear hierarchy** (session → repository → service)
7. ✅ **Reuse shared dependencies** (pagination, auth, session)
8. ✅ **Export all functions** in `__init__.py` for easy imports
9. ✅ Use **type hints everywhere** for IDE and type checking support
10. ✅ Support **testing** via dependency overrides

**Benefits of Dependency Injection:**
- **Loose Coupling**: Components depend on abstractions, not concrete implementations
- **Testability**: Easy to mock/override dependencies in tests
- **Maintainability**: Changes to implementations don't affect consumers
- **Separation of Concerns**: Clear boundaries between layers
- **Type Safety**: Full IDE support and static type checking
- **Lazy Evaluation**: Dependencies created only when needed
- **Framework Support**: FastAPI handles all the complexity

