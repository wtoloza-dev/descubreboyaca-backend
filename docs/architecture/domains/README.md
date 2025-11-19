# Domains Layer

## Purpose

The `app/domains/` layer contains **business logic** organized using **Clean Architecture** and **Domain-Driven Design (DDD)** principles. Each domain represents a bounded context in the business (restaurants, reviews, users, etc.).

## Architecture: Clean Architecture + DDD

**Core Concept**: Organize business logic in concentric layers where dependencies point inward (toward the domain core).

```
┌───────────────────────────────────────────┐
│   Presentation (Routes, Schemas)          │  Layer 4: Frameworks & Drivers
│   ┌───────────────────────────────────┐   │
│   │ Infrastructure (Repositories)     │   │  Layer 3: Interface Adapters
│   │   ┌───────────────────────────┐   │   │
│   │   │ Application (Use Cases)   │   │   │  Layer 2: Business Rules
│   │   │   ┌───────────────────┐   │   │   │
│   │   │   │ Domain (Entities) │   │   │   │  Layer 1: Enterprise Rules
│   │   │   └───────────────────┘   │   │   │
│   │   └───────────────────────────┘   │   │
│   └───────────────────────────────────┘   │
└───────────────────────────────────────────┘

Dependency Rule: Inner layers don't know about outer layers
```

## Available Domains

| Domain | Purpose | Bounded Context |
|--------|---------|-----------------|
| **audit** | Archive and audit logging | Entity archival system |
| **auth** | Authentication & authorization | User login, JWT, OAuth2 |
| **favorites** | User favorites management | Restaurant favorites |
| **restaurants** | Restaurant & dish management | Core business domain |
| **reviews** | Review and rating system | User feedback |
| **users** | User management | User profiles |

## Domain Structure

Each domain follows a consistent 4-layer structure:

```
app/domains/{domain}/
├── domain/                 # Layer 1: Enterprise Business Rules
│   ├── entities/           # Core business objects with identity
│   ├── value_objects/      # Immutable objects without identity
│   ├── interfaces/         # Repository contracts (Protocol)
│   ├── enums/             # Domain enumerations
│   └── exceptions/         # Domain-specific errors
│
├── application/            # Layer 2: Application Business Rules
│   ├── use_cases/         # Single-purpose operations (PREFERRED)
│   └── services/          # Complex domain logic (legacy)
│
├── infrastructure/         # Layer 3: Interface Adapters
│   ├── persistence/
│   │   ├── models/        # Database models (SQLModel)
│   │   └── repositories/  # Repository implementations
│   │       └── {entity}/
│   │           ├── common/sql.py     # Shared SQL logic
│   │           ├── postgresql.py     # PostgreSQL impl
│   │           └── sqlite.py         # SQLite impl
│   │
│   └── dependencies/      # Dependency injection
│       └── {subdomain}/
│           ├── repository.py   # Repository factory
│           └── use_cases.py    # Use case factories
│
└── presentation/           # Layer 4: Frameworks & Drivers
    └── api/
        ├── routes/        # FastAPI route handlers
        │   ├── admin/     # Admin endpoints
        │   ├── owner/     # Owner endpoints (if applicable)
        │   └── public/    # Public endpoints
        │
        └── schemas/       # Pydantic request/response models
            ├── admin/
            ├── owner/
            ├── public/
            └── common/
```

## Layer Responsibilities

### Layer 1: Domain Layer

**Rules**:
- ❌ NO external dependencies (FastAPI, SQLAlchemy, etc.)
- ❌ NO framework imports
- ✅ Pure Python business logic
- ✅ Framework-agnostic

**Contains**:
- **Entities**: Business objects with identity (e.g., `Restaurant`, `User`)
- **Value Objects**: Immutable objects (e.g., `ArchiveData`, `TokenData`)
- **Interfaces**: Repository contracts using `typing.Protocol`
- **Enums**: Domain enumerations (e.g., `UserRole`, `CuisineType`)
- **Exceptions**: Domain errors (e.g., `RestaurantNotFoundException`)

**Example Entity**:
```python
# app/domains/restaurants/domain/entities/restaurant.py

from pydantic import BaseModel, Field
from app.shared.domain.entities import Audit

class RestaurantData(BaseModel):
    """Restaurant data without system metadata."""
    name: str = Field(..., min_length=1, max_length=255)
    city: str
    cuisine_types: list[CuisineType] = Field(default_factory=list)
    price_level: int | None = Field(default=None, ge=1, le=4)

class Restaurant(RestaurantData, Audit):
    """Complete Restaurant entity with identity and audit trail.

    Attributes:
        id: ULID primary key (inherited from Audit)
        created_at: Timestamp (inherited from Audit)
        updated_at: Timestamp (inherited from Audit)
    """
```

**Example Interface**:
```python
# app/domains/restaurants/domain/interfaces/restaurant_repository.py

from typing import Protocol

class RestaurantRepositoryInterface(Protocol):
    """Contract for restaurant data access."""

    async def create(self, data: RestaurantData) -> Restaurant:
        """Create new restaurant."""
        ...

    async def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        """Find restaurant by ID."""
        ...

    async def update(self, restaurant: Restaurant) -> Restaurant:
        """Update restaurant."""
        ...
```

### Layer 2: Application Layer

**Rules**:
- ✅ Can import from domain layer
- ✅ Contains business logic orchestration
- ❌ NO web framework dependencies (FastAPI)
- ❌ NO database framework dependencies (SQLAlchemy)

**Contains**:
- **Use Cases**: Single-purpose operations (PREFERRED)
- **Services**: Complex domain logic (legacy, avoid for new features)

**Use Case Example**:
```python
# app/domains/restaurants/application/use_cases/create_restaurant.py

from app.domains.restaurants.domain import Restaurant, RestaurantData
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface

class CreateRestaurantUseCase:
    """Use case for creating a new restaurant."""

    def __init__(self, repository: RestaurantRepositoryInterface) -> None:
        """Initialize with repository dependency.

        Args:
            repository: Restaurant repository implementation
        """
        self.repository = repository

    async def execute(
        self,
        restaurant_data: RestaurantData,
        created_by: str | None = None,
    ) -> Restaurant:
        """Execute the create restaurant use case.

        Args:
            restaurant_data: Restaurant information
            created_by: User ID creating the restaurant

        Returns:
            Restaurant: The created restaurant entity

        Raises:
            RestaurantAlreadyExistsException: If restaurant exists
        """
        # Validation
        # Business logic
        # Persistence
        return await self.repository.create(restaurant_data, created_by=created_by)
```

**Use Case Characteristics**:
- ✅ Single responsibility (does ONE thing)
- ✅ Has one `execute()` method
- ✅ Receives dependencies via constructor
- ✅ Independent and testable
- ✅ Naming: `{Verb}{Noun}UseCase` (e.g., `CreateRestaurantUseCase`)

### Layer 3: Infrastructure Layer

**Rules**:
- ✅ Implements domain interfaces
- ✅ Framework-specific code (SQLAlchemy, FastAPI Depends)
- ✅ Adapts external systems to domain needs
- ✅ Dependencies point inward (toward domain)

**Contains**:
- **Models**: SQLModel database models (ORM)
- **Repositories**: Concrete repository implementations
- **Dependencies**: Dependency injection factories

**Repository Example**:
```python
# app/domains/restaurants/infrastructure/persistence/repositories/restaurant/postgresql.py

from sqlmodel.ext.asyncio.session import AsyncSession
from app.domains.restaurants.domain import Restaurant, RestaurantData
from app.domains.restaurants.domain.interfaces import RestaurantRepositoryInterface
from app.domains.restaurants.infrastructure.persistence.models import RestaurantModel

class PostgreSQLRestaurantRepository(RestaurantRepositoryInterface):
    """PostgreSQL implementation of restaurant repository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: RestaurantData, created_by: str | None = None) -> Restaurant:
        """Create restaurant in PostgreSQL."""
        model = RestaurantModel(**data.model_dump(), created_by=created_by)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        """Find restaurant by ID."""
        model = await self.session.get(RestaurantModel, restaurant_id)
        return self._to_entity(model) if model else None

    def _to_entity(self, model: RestaurantModel) -> Restaurant:
        """Convert database model to domain entity."""
        return Restaurant.model_validate(model)
```

**Dependency Factory Example**:
```python
# app/domains/restaurants/infrastructure/dependencies/restaurant/use_cases.py

from typing import Annotated
from fastapi import Depends

def get_create_restaurant_use_case_dependency(
    repository: Annotated[
        RestaurantRepositoryInterface,
        Depends(get_restaurant_repository_dependency)
    ],
) -> CreateRestaurantUseCase:
    """Factory to create CreateRestaurantUseCase instance."""
    return CreateRestaurantUseCase(repository)
```

### Layer 4: Presentation Layer

**Rules**:
- ✅ HTTP/REST specific code
- ✅ Request/response handling
- ✅ Depends on application layer (use cases)
- ✅ Validation with Pydantic schemas

**Contains**:
- **Routes**: FastAPI endpoint handlers
- **Schemas**: Pydantic request/response models

**Route Example**:
```python
# app/domains/restaurants/presentation/api/routes/admin/create.py

from typing import Annotated
from fastapi import APIRouter, Depends, status, Body
from app.domains.restaurants.application.use_cases import CreateRestaurantUseCase
from app.domains.restaurants.infrastructure.dependencies import (
    get_create_restaurant_use_case_dependency
)
from app.domains.restaurants.presentation.api.schemas import (
    CreateRestaurantSchemaRequest,
    CreateRestaurantSchemaResponse,
)

router = APIRouter()

@router.post("/restaurants", status_code=status.HTTP_201_CREATED)
async def handle_create_restaurant(
    request: Annotated[CreateRestaurantSchemaRequest, Body()],
    use_case: Annotated[
        CreateRestaurantUseCase,
        Depends(get_create_restaurant_use_case_dependency),
    ],
    admin_user: Annotated[User, Depends(require_admin_dependency)],
) -> CreateRestaurantSchemaResponse:
    """Create a new restaurant (Admin only)."""
    restaurant = await use_case.execute(
        restaurant_data=request.to_domain(),
        created_by=admin_user.id,
    )
    return CreateRestaurantSchemaResponse.from_entity(restaurant)
```

**Schema Example**:
```python
# app/domains/restaurants/presentation/api/schemas/admin/create.py

from pydantic import BaseModel
from app.domains.restaurants.domain import Restaurant, RestaurantData

class CreateRestaurantSchemaRequest(BaseModel):
    """Request schema for creating restaurant."""
    name: str
    city: str
    address: str
    phone: str

    def to_domain(self) -> RestaurantData:
        """Convert to domain entity data."""
        return RestaurantData(**self.model_dump())

class CreateRestaurantSchemaResponse(BaseModel):
    """Response schema for created restaurant."""
    id: str
    name: str
    city: str

    @classmethod
    def from_entity(cls, restaurant: Restaurant) -> "CreateRestaurantSchemaResponse":
        """Create from domain entity."""
        return cls(**restaurant.model_dump())
```

## Use Cases Pattern

### What is a Use Case?

A use case represents **ONE specific business operation** that a user (or system) can perform.

### Naming Convention

- **File**: `{verb}_{noun}.py` (e.g., `create_restaurant.py`)
- **Class**: `{Verb}{Noun}UseCase` (e.g., `CreateRestaurantUseCase`)

### Use Case Template

```python
class {Verb}{Noun}UseCase:
    """Use case for {description}."""

    def __init__(self, repository: RepositoryInterface) -> None:
        """Initialize with dependencies."""
        self.repository = repository

    async def execute(self, ...params) -> Result:
        """Execute the use case.

        Args:
            ...

        Returns:
            ...

        Raises:
            ...
        """
        # 1. Validate input
        # 2. Execute business logic
        # 3. Persist/retrieve data
        # 4. Return result
```

## Dependency Injection

### Structure by Subdomain

```
infrastructure/dependencies/
└── {subdomain}/           # e.g., restaurant/
    ├── __init__.py        # Export all dependencies
    ├── repository.py      # Repository factory
    └── use_cases.py       # Use case factories
```

### Repository Factory

```python
# infrastructure/dependencies/restaurant/repository.py

def get_restaurant_repository_dependency(
    session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
) -> RestaurantRepositoryInterface:
    """Factory to create restaurant repository."""
    if settings.SCOPE == "local":
        return SQLiteRestaurantRepository(session)
    else:
        return PostgreSQLRestaurantRepository(session)
```

### Use Case Factory

```python
# infrastructure/dependencies/restaurant/use_cases.py

def get_create_restaurant_use_case_dependency(
    repository: Annotated[
        RestaurantRepositoryInterface,
        Depends(get_restaurant_repository_dependency)
    ],
) -> CreateRestaurantUseCase:
    """Factory to create use case instance."""
    return CreateRestaurantUseCase(repository)
```

## Benefits

| Benefit | Description |
|---------|-------------|
| **Separation of Concerns** | Each layer has a single, well-defined purpose |
| **Testability** | Business logic can be tested without HTTP layer |
| **Framework Independence** | Domain logic doesn't depend on FastAPI |
| **Scalability** | Easy to add new features following the pattern |
| **AI-Friendly** | Predictable structure for AI code generation |
| **Maintainability** | Clear boundaries, easy to understand |

## Testing Strategy

### Unit Tests (Application Layer)

Test use cases in isolation with mock repositories:

```python
# tests/domains/restaurants/unit/use_cases/test_create_restaurant.py

async def test_create_restaurant_success(mock_repository):
    """Test creating restaurant successfully."""
    use_case = CreateRestaurantUseCase(repository=mock_repository)

    data = RestaurantData(name="Test", city="Tunja", ...)
    result = await use_case.execute(data)

    assert result.name == "Test"
    assert result.city == "Tunja"
```

### Integration Tests (Infrastructure Layer)

Test repositories with real database:

```python
# tests/domains/restaurants/integration/test_restaurant_repository.py

async def test_create_restaurant_in_db(db_session):
    """Test creating restaurant in database."""
    repository = SQLiteRestaurantRepository(db_session)

    data = RestaurantData(name="Test", city="Tunja", ...)
    result = await repository.create(data)

    assert result.id is not None
    assert result.created_at is not None
```

### E2E Tests (Presentation Layer)

Test full HTTP flow:

```python
# tests/domains/restaurants/e2e/test_create_restaurant_endpoint.py

async def test_create_restaurant_endpoint(client, admin_token):
    """Test creating restaurant via API."""
    response = await client.post(
        "/api/v1/admin/restaurants",
        json={"name": "Test", "city": "Tunja", ...},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test"
```

## Key Principles

1. **Dependency Rule**: Inner layers never depend on outer layers
2. **Single Responsibility**: Each use case does ONE thing
3. **Interface Segregation**: Small, focused repository interfaces
4. **Dependency Inversion**: Depend on abstractions (Protocol), not implementations
5. **Explicit Over Implicit**: Clear naming, no magic
6. **AI-First**: Predictable patterns for AI code generation

## Related Documentation

- [ARCHITECTURE.md - Section 4: Domains Layer](../../ARCHITECTURE.md#4-domains-layer-clean-architecture--ddd)
- [clients.md](./clients.md) - Database client layer
- [core.md](./core.md) - Framework infrastructure
- [shared.md](./shared.md) - Shared utilities
