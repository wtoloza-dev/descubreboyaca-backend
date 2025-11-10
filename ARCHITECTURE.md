# Architecture Documentation - Descubre Boyacá Backend

## Table of Contents

1. [Overview](#1-overview)
2. [Hybrid Architecture Approach](#2-hybrid-architecture-approach)
3. [Clients Layer (Hexagonal Architecture)](#3-clients-layer-hexagonal-architecture)
4. [Domains Layer (Clean Architecture + DDD)](#4-domains-layer-clean-architecture--ddd)
5. [Shared Components](#5-shared-components)
6. [Core Infrastructure](#6-core-infrastructure)
7. [Code Organization Guidelines](#7-code-organization-guidelines)
8. [Development Workflow](#8-development-workflow)
9. [Architecture Decision Records (ADRs)](#9-architecture-decision-records-adrs)
10. [Diagrams](#10-diagrams)

---

## 1. Overview

### 1.1 Project Vision

**Descubre Boyacá** is a backend API system designed to showcase and manage restaurants, reviews, and user experiences in Boyacá, Colombia. The system is built with scalability, maintainability, and clean code principles in mind.

The backend serves multiple client applications (web, mobile) through a RESTful API, providing:
- Restaurant management and discovery
- User authentication and authorization (JWT + OAuth2)
- Review and rating system
- Favorites management
- Audit and archival system

### 1.2 Architecture Philosophy

This project follows a **hybrid architecture approach**, combining different architectural patterns where they provide the most value:

**Core Philosophy:**
> "Use the right tool for the right job. Not every part of the system needs the same architectural complexity."

We prioritize:
- **Separation of Concerns**: Clear boundaries between layers
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Testability**: Easy to write unit and integration tests
- **Maintainability**: Code that's easy to understand and modify
- **Scalability**: Architecture that grows with the project

### 1.3 Key Principles

#### 1. Explicit Over Implicit
- Clear naming conventions (e.g., `ArchiveEntityUseCase` not just `Archive`)
- Explicit dependencies via constructor injection
- No magic or hidden behaviors

#### 2. Single Responsibility Principle (SRP)
- Each use case does ONE thing
- Each class has ONE reason to change
- Small, focused modules

#### 3. Dependency Inversion Principle (DIP)
- Depend on interfaces, not implementations
- Repositories implement domain interfaces
- Infrastructure depends on domain, never the reverse

#### 4. Domain-Centric Design
- Business logic lives in the domain layer
- Domain entities are independent of frameworks
- Infrastructure adapts to domain needs

#### 5. Type Safety
- Python 3.14 type hints everywhere
- Static type checking ready
- Runtime validation with Pydantic

#### 6. Documentation First
- Every module, class, and function has a docstring
- Google-style docstrings with examples
- Architecture decisions are documented

---

**Technology Stack:**
- **Language**: Python 3.14
- **Web Framework**: FastAPI
- **ORM**: SQLModel (built on SQLAlchemy 2.0)
- **Databases**: PostgreSQL (production), SQLite (development)
- **Authentication**: JWT with OAuth2 (Google) support
- **Validation**: Pydantic v2
- **Testing**: Pytest
- **Linting**: Ruff
- **Package Management**: uv

---

## 2. Hybrid Architecture Approach

### 2.1 Why Hybrid?

Instead of forcing a single architectural pattern across the entire codebase, we use different patterns where they make the most sense:

| Layer | Architecture | Reason |
|-------|-------------|--------|
| **Clients** | Hexagonal (Ports & Adapters) | Database adapters need to be swappable (PostgreSQL, SQLite, etc.) |
| **Domains** | Clean Architecture + DDD | Business logic needs to be isolated and testable |
| **Shared** | Utility Layer | Common code used across domains |
| **Core** | Infrastructure | Framework-specific configuration and setup |

### 2.2 Architecture Styles Used

#### Hexagonal Architecture (Ports & Adapters)
**Where**: `app/clients/` layer

**Purpose**: Isolate external dependencies (databases) from the application core.

**Key Concepts**:
- **Ports**: Interfaces that define contracts (e.g., `AsyncSQLClientPort`)
- **Adapters**: Concrete implementations (e.g., `AsyncPostgreSQLAdapter`, `AsyncSQLiteAdapter`)
- **Dependency Inversion**: The core doesn't know about specific databases

#### Clean Architecture
**Where**: `app/domains/` layer

**Purpose**: Organize business logic in layers with clear dependencies.

**Layers** (from inner to outer):
1. **Domain**: Entities, interfaces, exceptions (framework-independent)
2. **Application**: Use cases, services (business logic orchestration)
3. **Infrastructure**: Repositories, dependencies (framework-specific)
4. **Presentation**: API routes, schemas (HTTP/REST specific)

#### Domain-Driven Design (DDD)
**Where**: `app/domains/` layer

**Purpose**: Model the business domain accurately.

**Key Concepts**:
- **Entities**: Core business objects with identity (e.g., `User`, `Restaurant`)
- **Value Objects**: Immutable objects without identity (e.g., `ArchiveData`)
- **Repositories**: Data access interfaces
- **Use Cases**: Specific business operations
- **Domain Services**: Business logic that doesn't fit in entities

### 2.3 When to Use Each Style

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
  ┌──────────┐        ┌──────────┐       ┌──────────┐
  │  Domains │        │  Clients │       │  Shared  │
  │  (Clean  │        │(Hexagonal)│      │ (Utility)│
  │   Arch)  │        │          │       │          │
  └──────────┘        └──────────┘       └──────────┘
        │                   │
        └─────────┬─────────┘
                  ▼
          ┌──────────────┐
          │  Core (Infra)│
          └──────────────┘
```

**Use Hexagonal when**:
- You need to swap implementations (databases, message queues, external APIs)
- You want to isolate infrastructure concerns
- Testing with different adapters is important

**Use Clean Architecture when**:
- You have complex business logic
- You need clear separation between layers
- Domain logic should be framework-independent

**Use Simple Utility when**:
- Code is shared across domains
- No complex business logic involved
- Just helper functions or common patterns

---

## 3. Clients Layer (Hexagonal Architecture)

### 3.1 Ports and Adapters Pattern

The `app/clients/` layer implements **Hexagonal Architecture** (also known as Ports and Adapters).

```
app/clients/
└── sql/
    ├── ports/              # Interfaces (Ports)
    │   ├── asynchronous.py # AsyncSQLClientPort
    │   └── synchronous.py  # SyncSQLClientPort
    │
    ├── adapters/           # Implementations (Adapters)
    │   ├── postgres/
    │   │   ├── asynchronous.py  # AsyncPostgreSQLAdapter
    │   │   └── synchronous.py   # SyncPostgreSQLAdapter
    │   └── sqlite/
    │       ├── asynchronous.py  # AsyncSQLiteAdapter
    │       └── synchronous.py   # SyncSQLiteAdapter
    │
    └── dependencies/       # Dependency Injection factories
        ├── postgres.py
        └── sqlite.py
```

### 3.2 Key Components

#### Ports (Interfaces)

**Purpose**: Define the contract that all database adapters must implement.

**Example**: `AsyncSQLClientPort`
```python
class AsyncSQLClientPort(Protocol):
    """Port (interface) for async SQL database clients."""
    
    def connect(self) -> None:
        """Establish database connection."""
        ...
    
    async def disconnect(self) -> None:
        """Close database connection."""
        ...
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        ...
```

#### Adapters (Implementations)

**Purpose**: Implement the port for specific database technologies.

**Example**: `AsyncPostgreSQLAdapter`
```python
class AsyncPostgreSQLAdapter:
    """PostgreSQL adapter implementing AsyncSQLClientPort."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine: AsyncEngine | None = None
    
    def connect(self) -> None:
        self.engine = create_async_engine(self.database_url)
    
    async def disconnect(self) -> None:
        if self.engine:
            await self.engine.dispose()
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            yield session
```

### 3.3 Benefits

✅ **Swappable**: Change from PostgreSQL to SQLite without touching domain code  
✅ **Testable**: Easy to create mock adapters for testing  
✅ **Isolated**: Database-specific code is contained in adapters  
✅ **Flexible**: Add new databases by creating new adapters  

### 3.4 Adding a New Database Adapter

1. Create adapter file: `app/clients/sql/adapters/mysql/asynchronous.py`
2. Implement the port: `AsyncSQLClientPort`
3. Add dependency factory: `app/clients/sql/dependencies/mysql.py`
4. Register in settings

---

## 4. Domains Layer (Clean Architecture + DDD)

### 4.1 Domain-Driven Design Principles

Each domain represents a **bounded context** in the business:
- `audit`: Archive and audit logging
- `auth`: Authentication and authorization
- `favorites`: User favorites management
- `restaurants`: Restaurant and dish management
- `reviews`: Review and rating system
- `users`: User management

### 4.2 Layer Responsibilities

Each domain follows **Clean Architecture** with these layers:

```
app/domains/{domain}/
├── domain/              # Layer 1: Enterprise Business Rules
│   ├── entities/        # Core business objects with identity
│   ├── value_objects/   # Immutable objects without identity
│   ├── interfaces/      # Repository and service interfaces
│   ├── enums/          # Domain enumerations
│   └── exceptions/      # Domain-specific exceptions
│
├── application/         # Layer 2: Application Business Rules
│   ├── use_cases/      # Specific business operations (PREFERRED)
│   └── services/       # Domain services (legacy, for complex logic)
│
├── infrastructure/      # Layer 3: Interface Adapters
│   ├── persistence/
│   │   ├── models/     # Database models (SQLModel)
│   │   └── repositories/ # Repository implementations
│   └── dependencies/   # Dependency injection factories
│       └── {subdomain}/
│           ├── repository.py
│           ├── service.py
│           └── use_cases.py
│
└── presentation/        # Layer 4: Frameworks & Drivers
    └── api/
        ├── routes/     # FastAPI route handlers
        └── schemas/    # Pydantic request/response schemas
```

#### Layer 1: Domain Layer

**Rules**:
- ❌ NO external dependencies (FastAPI, SQLAlchemy, etc.)
- ❌ NO framework imports
- ✅ Pure Python business logic
- ✅ Framework-agnostic

**Contains**:
- **Entities**: Business objects with identity (e.g., `User`, `Restaurant`)
- **Value Objects**: Immutable objects (e.g., `ArchiveData`, `TokenData`)
- **Interfaces**: Contracts (e.g., `UserRepositoryInterface`)
- **Enums**: Domain enumerations (e.g., `UserRole`, `AuthProvider`)
- **Exceptions**: Domain errors (e.g., `UserNotFoundException`)

**Example**: `app/domains/users/domain/entities/user.py`
```python
class User:
    """User entity representing a system user."""
    
    def __init__(
        self,
        id: str,
        email: str,
        role: UserRole,
        is_active: bool = True,
    ) -> None:
        self.id = id
        self.email = email
        self.role = role
        self.is_active = is_active
    
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN
```

#### Layer 2: Application Layer

**Rules**:
- ✅ Can import from domain layer
- ✅ Contains business logic orchestration
- ❌ NO web framework dependencies (FastAPI)
- ❌ NO database framework dependencies (SQLAlchemy)

**Contains**:
- **Use Cases**: Single-purpose operations (PREFERRED)
- **Services**: Complex domain logic that doesn't fit in entities (legacy)

**Use Case Example**: `app/domains/audit/application/use_cases/archive_entity.py`
```python
class ArchiveEntityUseCase:
    """Use case for archiving a deleted entity."""
    
    def __init__(self, repository: ArchiveRepositoryInterface) -> None:
        self.repository = repository
    
    async def execute(
        self,
        table_name: str,
        entity: BaseModel,
        note: str | None = None,
        deleted_by: str | None = None,
    ) -> Archive:
        """Execute the archive entity use case."""
        # Validation
        if not hasattr(entity, "id"):
            raise AttributeError("Entity must have an 'id' field")
        
        # Business logic
        entity_data = entity.model_dump(mode="json")
        archive_data = ArchiveData(
            original_table=table_name,
            original_id=str(entity.id),
            data=entity_data,
            note=note,
        )
        
        # Persistence
        return await self.repository.create(archive_data, deleted_by=deleted_by)
```

#### Layer 3: Infrastructure Layer

**Rules**:
- ✅ Implements domain interfaces
- ✅ Framework-specific code (SQLAlchemy, FastAPI dependencies)
- ✅ Adapts external systems to domain needs

**Contains**:
- **Models**: SQLModel database models
- **Repositories**: Concrete repository implementations
- **Dependencies**: Dependency injection factories

**Repository Example**: `app/domains/users/infrastructure/persistence/repositories/user/sqlite.py`
```python
class SQLiteUserRepository(UserRepositoryInterface):
    """SQLite implementation of UserRepositoryInterface."""
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def find_by_email(self, email: str) -> User | None:
        """Find user by email."""
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.exec(query)
        model = result.first()
        
        if not model:
            return None
        
        return self._to_entity(model)
```

#### Layer 4: Presentation Layer

**Rules**:
- ✅ HTTP/REST specific code
- ✅ Request/response handling
- ✅ Depends on application layer (use cases)

**Contains**:
- **Routes**: FastAPI endpoint handlers
- **Schemas**: Pydantic request/response models

**Route Example**: `app/domains/audit/presentation/api/routes/admin/hard_delete.py`
```python
@router.delete("/archives", status_code=status.HTTP_200_OK)
async def handle_hard_delete_archive(
    request: Annotated[HardDeleteArchiveSchemaRequest, Body()],
    use_case: Annotated[
        HardDeleteArchiveByOriginalIdUseCase,
        Depends(get_hard_delete_archive_by_original_id_use_case_dependency),
    ],
    admin_user: Annotated[User, Depends(require_admin_dependency)],
) -> HardDeleteArchiveSchemaResponse:
    """Handle hard delete archive request."""
    deleted = await use_case.execute(
        original_table=request.original_table,
        original_id=request.original_id,
    )
    
    return HardDeleteArchiveSchemaResponse(
        success=deleted,
        message=f"Archive deleted" if deleted else "Not found",
    )
```

### 4.3 Use Cases Pattern

**What is a Use Case?**

A use case represents **ONE specific business operation** that a user (or system) can perform.

**Characteristics**:
- ✅ Single responsibility (does one thing)
- ✅ Has an `execute()` method
- ✅ Receives dependencies via constructor
- ✅ Contains business logic orchestration
- ✅ Independent and testable

**Naming Convention**:
- **File**: `{verb}_{noun}.py` (e.g., `archive_entity.py`)
- **Class**: `{Verb}{Noun}UseCase` (e.g., `ArchiveEntityUseCase`)

**Structure**:
```python
class ArchiveEntityUseCase:
    """Use case for archiving a deleted entity."""
    
    def __init__(self, repository: ArchiveRepositoryInterface) -> None:
        """Initialize with dependencies."""
        self.repository = repository
    
    async def execute(self, ...params) -> Result:
        """Execute the use case."""
        # 1. Validate input
        # 2. Execute business logic
        # 3. Persist/retrieve data
        # 4. Return result
```

**Example Use Cases**:
- `ArchiveEntityUseCase` - Archive a deleted entity
- `FindArchiveByOriginalIdUseCase` - Find an archived record
- `HardDeleteArchiveByOriginalIdUseCase` - Permanently delete archive
- `CreateUserUseCase` - Create a new user
- `AuthenticateUserUseCase` - Authenticate user credentials

### 4.4 Service Pattern (Legacy)

**What is a Service?**

A service contains **complex domain logic** that doesn't naturally belong to an entity or value object.

**When to Use Services**:
- Complex calculations spanning multiple entities
- Business logic that doesn't fit in a single use case
- Shared logic used by multiple use cases

**Current Status**: Legacy pattern, prefer **Use Cases** for new features.

**Example** (acceptable service):
```python
class PricingService:
    """Service for complex pricing calculations."""
    
    def calculate_total_price(
        self,
        base_price: Decimal,
        discount: Decimal,
        tax_rate: Decimal,
    ) -> Decimal:
        """Calculate final price with discount and tax."""
        discounted = base_price * (1 - discount)
        return discounted * (1 + tax_rate)
```

### 4.5 Dependency Injection

**Structure**: Dependencies are organized by subdomain:

```
infrastructure/dependencies/
└── {subdomain}/           # e.g., archive/
    ├── __init__.py        # Export all dependencies
    ├── repository.py      # Repository factory
    ├── service.py         # Service factory (legacy)
    └── use_cases.py       # Use case factories
```

**Example**: `app/domains/audit/infrastructure/dependencies/archive/use_cases.py`
```python
def get_archive_entity_use_case_dependency(
    repository: Annotated[
        ArchiveRepositoryInterface,
        Depends(get_archive_repository_dependency)
    ],
) -> ArchiveEntityUseCase:
    """Factory to create ArchiveEntityUseCase instance."""
    return ArchiveEntityUseCase(repository)
```

**Usage in Routes**:
```python
async def handle_request(
    use_case: Annotated[
        ArchiveEntityUseCase,
        Depends(get_archive_entity_use_case_dependency),
    ],
):
    result = await use_case.execute(...)
```

---

## 5. Shared Components

### 5.1 Purpose

The `app/shared/` layer contains code that is used across **multiple domains** but doesn't belong to any specific domain.

```
app/shared/
├── dependencies/       # Shared dependencies (pagination, SQL session)
├── domain/
│   ├── constants/      # System-wide constants
│   ├── entities/       # Base entities (AuditMixin)
│   ├── enums/         # Shared enums
│   ├── exceptions/     # Base exceptions
│   ├── factories/      # ID and datetime generators
│   ├── patterns/       # Unit of Work, etc.
│   └── value_objects/  # Pagination, etc.
├── models/            # Base SQLModel classes
└── schemas/           # Base Pydantic schemas
```

### 5.2 Domain Primitives

#### Entities
- `AuditMixin`: Base class with audit fields (created_at, updated_at, etc.)

#### Exceptions
- `DomainException`: Base exception for all domain errors
- `NotFoundException`: Resource not found
- `AlreadyExistsException`: Resource already exists
- `UnauthorizedException`: Authentication error
- `ForbiddenException`: Authorization error
- `ValidationException`: Validation error

#### Factories
- `generate_ulid()`: Create ULID identifiers
- `utc_now()`: Get current UTC datetime

#### Value Objects
- `Pagination`: Pagination parameters (page, page_size)
- `Address`: Address value object
- `Coordinates`: Geographic coordinates

### 5.3 Common Patterns

#### Unit of Work Pattern
```python
class UnitOfWork:
    """Unit of Work pattern for managing transactions."""
    
    async def __aenter__(self):
        """Start transaction."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Commit or rollback transaction."""
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
```

### 5.4 Dependencies

#### SQL Session Dependency
```python
async def get_async_session_dependency(
    client: Annotated[AsyncSQLClient, Depends(get_async_sql_client)],
) -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    async with client.get_session() as session:
        yield session
```

#### Pagination Dependency
```python
def get_pagination_dependency(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> Pagination:
    """Get pagination parameters."""
    return Pagination(page=page, page_size=page_size)
```

---

## 6. Core Infrastructure

### 6.1 Purpose

The `app/core/` layer contains **framework-specific** configuration and infrastructure that doesn't belong to any domain.

```
app/core/
├── settings/           # Environment configuration
│   ├── base.py        # Base settings
│   ├── local.py       # Local/dev settings
│   ├── staging.py     # Staging settings
│   └── prod.py        # Production settings
│
├── errors/            # Global error handling
│   ├── handlers.py    # FastAPI exception handlers
│   └── mappers.py     # Map domain exceptions to HTTP
│
└── lifespan.py        # Application startup/shutdown
```

### 6.2 Settings Management

**Environment-based configuration** using Pydantic Settings:

```python
class Settings(BaseSettings):
    """Base application settings."""
    
    # Environment
    SCOPE: str = Field(default="local")
    
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30
    
    # OAuth
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
```

**Loading Settings**:
```python
from app.core.settings import settings

database_url = settings.DATABASE_URL
```

### 6.3 Error Handling System

**Domain Exception → HTTP Response**:

```python
# Domain layer raises exception
raise UserNotFoundException(user_id="123")

# Error mapper converts to HTTP
{
    "detail": "User not found",
    "status_code": 404,
    "error_code": "USER_NOT_FOUND"
}
```

**Exception Handlers**:
```python
@app.exception_handler(NotFoundException)
async def not_found_handler(
    request: Request,
    exc: NotFoundException,
) -> JSONResponse:
    """Handle 404 Not Found exceptions."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )
```

### 6.4 Application Lifespan

**Startup and Shutdown Events**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan."""
    # Startup
    sql_client.connect()
    logger.info("Database connected")
    
    yield
    
    # Shutdown
    await sql_client.disconnect()
    logger.info("Database disconnected")
```

---

## 7. Code Organization Guidelines

### 7.1 File Naming Conventions

#### Use Cases
- **File**: lowercase with underscores, descriptive verb + noun
  - ✅ `archive_entity.py`
  - ✅ `find_archive_by_original_id.py`
  - ❌ `archive.py` (too vague)
  - ❌ `find.py` (incomplete)

- **Class**: PascalCase with `UseCase` suffix
  - ✅ `ArchiveEntityUseCase`
  - ✅ `FindArchiveByOriginalIdUseCase`
  - ❌ `ArchiveUseCase` (too vague)

#### Repositories
- **File**: lowercase with underscores, technology name
  - ✅ `sqlite.py`
  - ✅ `postgresql.py`

- **Class**: PascalCase with technology and `Repository`
  - ✅ `SQLiteUserRepository`
  - ✅ `PostgreSQLUserRepository`

#### Entities
- **File**: lowercase singular
  - ✅ `user.py`
  - ✅ `restaurant.py`

- **Class**: PascalCase singular
  - ✅ `User`
  - ✅ `Restaurant`

#### Dependencies
- **File**: lowercase with context
  - ✅ `repository.py`
  - ✅ `use_cases.py`

- **Function**: `get_{name}_dependency`
  - ✅ `get_archive_repository_dependency()`
  - ✅ `get_archive_entity_use_case_dependency()`

### 7.2 Import Organization

**Order** (enforced by Ruff):
1. Standard library imports
2. Third-party imports
3. Local application imports

**Example**:
```python
# Standard library
from datetime import UTC, datetime
from typing import Any

# Third-party
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# Local
from app.domains.audit.domain import Archive
from app.domains.audit.infrastructure.dependencies import (
    get_archive_repository_dependency,
)
```

### 7.3 Documentation Standards

**Every module must have a docstring**:
```python
"""Module description.

Longer description explaining what this module does,
what it contains, and how it fits in the system.
"""
```

**Every class must have a docstring**:
```python
class ArchiveEntityUseCase:
    """Use case for archiving a deleted entity.
    
    This use case handles the complete workflow of archiving
    an entity when it's deleted from the system.
    
    Attributes:
        repository: Archive repository for data persistence
    
    Example:
        >>> use_case = ArchiveEntityUseCase(repository)
        >>> archive = await use_case.execute(...)
    """
```

**Every public function/method must have a docstring**:
```python
async def execute(
    self,
    table_name: str,
    entity: BaseModel,
) -> Archive:
    """Execute the archive entity use case.
    
    Args:
        table_name: Name of the source table
        entity: The entity being deleted
    
    Returns:
        Archive: The created archive record
    
    Raises:
        AttributeError: If entity lacks 'id' field
    
    Example:
        >>> archive = await use_case.execute("restaurants", restaurant)
    """
```

**Type Hints**: Required on all function signatures:
```python
# ✅ Good
async def create_user(name: str, email: str) -> User:
    ...

# ❌ Bad
async def create_user(name, email):
    ...
```

---

## 8. Development Workflow

### 8.1 Adding a New Domain

**Steps**:

1. **Create domain structure**:
```bash
mkdir -p app/domains/{domain}/{domain,application,infrastructure,presentation}
```

2. **Create subdirectories**:
```bash
# Domain layer
mkdir -p app/domains/{domain}/domain/{entities,interfaces,exceptions,enums}

# Application layer
mkdir -p app/domains/{domain}/application/{use_cases,services}

# Infrastructure layer
mkdir -p app/domains/{domain}/infrastructure/{persistence,dependencies}
mkdir -p app/domains/{domain}/infrastructure/persistence/{models,repositories}

# Presentation layer
mkdir -p app/domains/{domain}/presentation/api/{routes,schemas}
```

3. **Add `__init__.py` with docstrings** to each directory

4. **Define domain entities** in `domain/entities/`

5. **Define repository interfaces** in `domain/interfaces/`

6. **Create use cases** in `application/use_cases/`

7. **Implement repositories** in `infrastructure/persistence/repositories/`

8. **Create dependencies** in `infrastructure/dependencies/`

9. **Add API routes** in `presentation/api/routes/`

10. **Register routes** in `app/main.py`

### 8.2 Adding a New Use Case

**Example**: Adding `FindAllArchivesUseCase` to the `audit` domain

**Step 1**: Create use case file
```bash
touch app/domains/audit/application/use_cases/find_all_archives.py
```

**Step 2**: Implement use case
```python
"""Find all archives use case."""

from app.domains.audit.domain import Archive, ArchiveRepositoryInterface
from app.shared.domain.value_objects import Pagination


class FindAllArchivesUseCase:
    """Use case for finding all archives with pagination."""
    
    def __init__(self, repository: ArchiveRepositoryInterface) -> None:
        """Initialize use case.
        
        Args:
            repository: Archive repository implementation
        """
        self.repository = repository
    
    async def execute(
        self,
        pagination: Pagination,
    ) -> list[Archive]:
        """Execute the find all archives use case.
        
        Args:
            pagination: Pagination parameters
        
        Returns:
            list[Archive]: List of archive records
        """
        return await self.repository.find_all(
            offset=pagination.offset,
            limit=pagination.page_size,
        )
```

**Step 3**: Add to `use_cases/__init__.py`
```python
from app.domains.audit.application.use_cases.find_all_archives import (
    FindAllArchivesUseCase,
)

__all__ = [
    # ... existing
    "FindAllArchivesUseCase",
]
```

**Step 4**: Create dependency
```python
# In infrastructure/dependencies/archive/use_cases.py

def get_find_all_archives_use_case_dependency(
    repository: Annotated[
        ArchiveRepositoryInterface,
        Depends(get_archive_repository_dependency),
    ],
) -> FindAllArchivesUseCase:
    """Factory to create FindAllArchivesUseCase instance."""
    return FindAllArchivesUseCase(repository)
```

**Step 5**: Export dependency
```python
# In infrastructure/dependencies/archive/__init__.py

from app.domains.audit.infrastructure.dependencies.archive.use_cases import (
    # ... existing
    get_find_all_archives_use_case_dependency,
)

__all__ = [
    # ... existing
    "get_find_all_archives_use_case_dependency",
]
```

**Step 6**: Create route
```python
# In presentation/api/routes/admin/find_all_archives.py

@router.get("/archives", status_code=status.HTTP_200_OK)
async def handle_find_all_archives(
    use_case: Annotated[
        FindAllArchivesUseCase,
        Depends(get_find_all_archives_use_case_dependency),
    ],
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
) -> FindAllArchivesSchemaResponse:
    """Find all archives with pagination."""
    archives = await use_case.execute(pagination)
    return FindAllArchivesSchemaResponse(archives=archives)
```

### 8.3 Creating Dependencies

**Dependency Structure** (by subdomain):

```
infrastructure/dependencies/
└── {subdomain}/
    ├── __init__.py        # Export all
    ├── repository.py      # Repository dependency
    ├── service.py         # Service dependency (optional)
    └── use_cases.py       # All use case dependencies
```

**Example**: `repository.py`
```python
def get_archive_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> ArchiveRepositoryInterface:
    """Factory to create archive repository instance."""
    if settings.SCOPE == "local":
        return SQLiteArchiveRepository(session)
    else:
        return PostgreSQLArchiveRepository(session)
```

### 8.4 Testing Strategy

**Unit Tests**: Test individual components in isolation
```python
# tests/domains/audit/unit/use_cases/test_archive_entity.py

async def test_archive_entity_success(mock_repository):
    """Test archiving entity successfully."""
    use_case = ArchiveEntityUseCase(repository=mock_repository)
    
    entity = Restaurant(id="123", name="Test")
    result = await use_case.execute("restaurants", entity)
    
    assert result.original_table == "restaurants"
    assert result.original_id == "123"
```

**Integration Tests**: Test with real database
```python
# tests/domains/audit/integration/test_archive_repository.py

async def test_create_archive(db_session):
    """Test creating archive in database."""
    repository = SQLiteArchiveRepository(db_session)
    
    archive_data = ArchiveData(...)
    result = await repository.create(archive_data)
    
    assert result.id is not None
```

---

## 9. Architecture Decision Records (ADRs)

### 9.1 Why Use Cases over Services?

**Decision**: Prefer Use Cases for new features, keep Services for complex domain logic only.

**Context**:
- Services tend to grow too large (many methods)
- Hard to test a service with 10+ methods
- Violates Single Responsibility Principle

**Consequences**:
✅ Each use case is focused and testable  
✅ Clear boundaries for business operations  
✅ Easier to understand and maintain  
✅ Better for parallel development  
❌ More files (but better organized)

**Example**:
```python
# ❌ Service with multiple responsibilities
class ArchiveService:
    def archive_entity(...)
    def hard_delete_by_original_id(...)
    def find_by_original_id(...)
    def find_all(...)
    def restore_archive(...)

# ✅ Separate use cases
class ArchiveEntityUseCase: ...
class HardDeleteArchiveByOriginalIdUseCase: ...
class FindArchiveByOriginalIdUseCase: ...
class FindAllArchivesUseCase: ...
class RestoreArchiveUseCase: ...
```

### 9.2 Why Hexagonal Architecture for Clients?

**Decision**: Use Hexagonal Architecture (Ports & Adapters) for `app/clients/`.

**Context**:
- Need to support multiple databases (PostgreSQL, SQLite)
- Want to easily swap implementations
- Testing requires mock databases

**Consequences**:
✅ Database-agnostic domain code  
✅ Easy to add new databases  
✅ Simple to create test adapters  
✅ Clear separation of concerns  
❌ Additional abstraction layer

### 9.3 Why Clean Architecture for Domains?

**Decision**: Use Clean Architecture for `app/domains/`.

**Context**:
- Complex business logic across multiple domains
- Need framework-independent domain layer
- Want testable business logic

**Consequences**:
✅ Domain logic independent of FastAPI  
✅ Easy to test without HTTP layer  
✅ Clear dependency direction (inward)  
✅ Scalable for complex domains  
❌ More directories and layers

### 9.4 Dependency Injection Strategy

**Decision**: Use FastAPI's `Depends()` for dependency injection, organized by subdomain.

**Context**:
- Need to inject repositories, use cases into routes
- Want environment-specific implementations (SQLite vs PostgreSQL)
- Keep related dependencies together

**Structure**:
```
dependencies/{subdomain}/
├── repository.py   # Database selection logic
├── use_cases.py    # Use case factories
└── service.py      # Service factories (legacy)
```

**Consequences**:
✅ Clear organization by subdomain  
✅ Easy to find dependencies  
✅ Scalable for growing domains  
✅ Type-safe dependency injection  
❌ More files per subdomain

---

## 10. Diagrams

### 10.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI Application                        │
│                         (app/main.py)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Domains    │    │   Clients    │    │    Shared    │
│   (Clean     │    │ (Hexagonal)  │    │  (Utility)   │
│    Arch)     │    │              │    │              │
└──────┬───────┘    └──────┬───────┘    └──────────────┘
       │                   │
       │                   │
       └────────┬──────────┘
                │
                ▼
        ┌──────────────┐
        │     Core     │
        │    (Infra)   │
        └──────────────┘
                │
                ▼
        ┌──────────────┐
        │  PostgreSQL  │
        │   / SQLite   │
        └──────────────┘
```

### 10.2 Domain Layer Structure

```
Domain (audit)
│
├── domain/                    [Layer 1: Enterprise Business Rules]
│   ├── entities/              • Archive
│   ├── interfaces/            • ArchiveRepositoryInterface
│   └── exceptions/            • ArchiveNotFoundException
│
├── application/               [Layer 2: Application Business Rules]
│   ├── use_cases/
│   │   ├── archive_entity.py              (ArchiveEntityUseCase)
│   │   ├── find_archive_by_original_id.py (FindArchiveByOriginalIdUseCase)
│   │   └── hard_delete_archive_by_original_id.py
│   │
│   └── services/              • Complex domain logic (optional)
│
├── infrastructure/            [Layer 3: Interface Adapters]
│   ├── persistence/
│   │   ├── models/            • ArchiveModel (SQLModel)
│   │   └── repositories/      • SQLiteArchiveRepository
│   │
│   └── dependencies/
│       └── archive/
│           ├── repository.py   (get_archive_repository_dependency)
│           └── use_cases.py    (get_*_use_case_dependency)
│
└── presentation/              [Layer 4: Frameworks & Drivers]
    └── api/
        ├── routes/            • FastAPI routes
        └── schemas/           • Pydantic schemas
```

**Dependency Direction**: Always points **inward** (toward domain)
```
Presentation → Application → Domain
Infrastructure → Domain
```

### 10.3 Clients Hexagonal Architecture

```
                    ┌─────────────────────┐
                    │  Domain Layer       │
                    │  (Uses Port)        │
                    └──────────┬──────────┘
                               │
                               │ depends on
                               │
                    ┌──────────▼──────────┐
                    │   Port (Interface)  │
                    │  AsyncSQLClientPort │
                    └──────────┬──────────┘
                               │
                               │ implements
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Adapter     │    │   Adapter     │    │   Adapter     │
│  PostgreSQL   │    │    SQLite     │    │  (Future DB)  │
└───────┬───────┘    └───────┬───────┘    └───────────────┘
        │                    │
        ▼                    ▼
┌───────────────┐    ┌───────────────┐
│  PostgreSQL   │    │    SQLite     │
│   Database    │    │   Database    │
└───────────────┘    └───────────────┘
```

**Key**:
- **Port**: Interface defining the contract
- **Adapter**: Implementation for specific technology
- **Domain**: Uses port, doesn't know about adapters

### 10.4 Request Flow Diagram

```
1. HTTP Request
   │
   ▼
2. FastAPI Route (Presentation Layer)
   │
   ├─ Validate request (Pydantic schema)
   ├─ Inject dependencies (Depends)
   │
   ▼
3. Use Case (Application Layer)
   │
   ├─ Validate business rules
   ├─ Execute business logic
   │
   ▼
4. Repository (Infrastructure Layer)
   │
   ├─ Convert to database model
   ├─ Execute SQL query
   │
   ▼
5. Database Adapter (Clients Layer)
   │
   ├─ Execute query via SQLAlchemy
   │
   ▼
6. Database (PostgreSQL/SQLite)
   │
   ▼
7. Response Flow (reverse direction)
   │
   ├─ Database → Adapter → Repository → Use Case → Route
   │
   ▼
8. HTTP Response (Pydantic schema)
```

**Example**: Hard Delete Archive

```
DELETE /api/v1/admin/archives
   │
   ▼
handle_hard_delete_archive()                [Presentation]
   │
   ├─ Validate: HardDeleteArchiveSchemaRequest
   ├─ Inject: HardDeleteArchiveByOriginalIdUseCase
   ├─ Auth: require_admin_dependency
   │
   ▼
HardDeleteArchiveByOriginalIdUseCase        [Application]
   │
   ├─ use_case.execute(table_name, original_id)
   │
   ▼
ArchiveRepositoryInterface                  [Domain]
   │
   ├─ repository.hard_delete(filters)
   │
   ▼
SQLiteArchiveRepository                     [Infrastructure]
   │
   ├─ Convert filters to SQL WHERE clause
   ├─ session.delete(model)
   ├─ session.commit()
   │
   ▼
AsyncSQLiteAdapter                          [Clients]
   │
   ├─ Execute via SQLAlchemy
   │
   ▼
SQLite Database
   │
   ▼
Response: { "success": true, "message": "..." }
```

---

## Contributing

When contributing to this project:

1. **Follow the architecture** patterns described in this document
2. **Maintain layer boundaries**: Don't import from outer layers into inner layers
3. **Write tests**: Unit tests for use cases, integration tests for repositories
4. **Document your code**: Every public class and method needs a docstring
5. **Use type hints**: All function signatures must have type annotations
6. **Run linters**: `make lint` and `make fix` before committing
7. **Update this document** if you make architectural changes

---

## Questions?

For questions about architecture decisions, consult:
- This document
- Code examples in existing domains
- Team lead or senior developers

**Last Updated**: 2025-01-07

