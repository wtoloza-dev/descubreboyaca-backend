# Architecture

This document describes the architecture of the Descubre Boyacá backend, which implements a **hybrid approach** combining multiple architectural patterns according to the needs of each layer.

## 📐 Overview

The project uses a **hybrid architecture** that combines:

- **Hexagonal Architecture** (Ports & Adapters) for external communications
- **Domain-Driven Design (DDD)** with **Vertical Slicing** for business domains
- **Clean Architecture** (Layered) within each component, without explicit layer folders

```
app/
├── clients/          → Hexagonal Architecture (external communications)
├── core/             → Application configuration and settings
├── shared/           → Shared components (Clean Layered)
├── domains/          → DDD + Vertical Slicing (Clean Layered)
└── main.py           → Entry point
```

---

## 🔌 Clients Layer - Hexagonal Architecture

**Purpose**: Handle communications with external systems (databases, APIs, services).

**Pattern**: **Hexagonal Architecture** (Ports & Adapters Pattern)

### Structure:

```
clients/
└── sql/
    ├── ports/              → Interfaces (Protocols) - Contracts
    │   ├── sql.py          → SQLClientProtocol
    │   └── async_sql.py    → AsyncSQLClientProtocol
    │
    ├── adapters/           → Concrete implementations
    │   ├── sqlite_client.py    → SQLiteClient, AsyncSQLiteClient
    │   └── postgres_client.py  → PostgreSQLClient, AsyncPostgreSQLClient
    │
    └── dependencies/       → Factories for dependency injection
        └── sqlite.py       → get_sqlite_session_dependency()
```

### Principles:

- **Ports** (interfaces) define the contract
- **Adapters** (implementations) fulfill the contract
- The application depends on **Ports**, not **Adapters**
- Easy to swap implementations (SQLite ↔ PostgreSQL ↔ MySQL)

### Example:

```python
# Port (abstraction)
class SQLClientProtocol(Protocol):
    def get_session(self) -> Generator[Session]: ...

# Adapters (implementations)
class SQLiteClient:
    def get_session(self) -> Generator[Session]: ...

class PostgreSQLClient:
    def get_session(self) -> Generator[Session]: ...
```

---

## ⚙️ Core Layer

**Purpose**: Global application configuration.

**Contents**:
- `settings/` - Environment-specific configurations (local, staging, prod)
- `routes/` - Main route registration

```
core/
├── settings/
│   ├── base.py       → Base configuration
│   ├── local.py      → Local/development configuration
│   ├── staging.py    → Staging configuration
│   └── prod.py       → Production configuration
└── routes/
    └── main.py       → Main router
```

---

## 🌐 Shared Layer - Clean Architecture (Layered)

**Purpose**: Components shared across multiple domains.

**Pattern**: **Clean Architecture** with implicit layers (without domain/application/infrastructure folders).

### Structure:

```
shared/
├── entities/             → Domain Layer - Business entities
│   ├── archive.py        → ArchiveData, Archive
│   └── audit.py          → Audit (base entity)
│
├── interfaces/           → Domain Layer - Contracts (Protocols)
│   └── archive.py        → ArchiveRepositoryProtocol
│
├── models/               → Infrastructure Layer - ORM
│   ├── archive.py        → ArchiveModel (SQLModel)
│   └── audit.py          → AuditMixin (SQLModel)
│
├── repositories/         → Infrastructure Layer - Persistence
│   └── archive.py        → ArchiveRepository
│
├── services/             → Application Layer - Business logic
│   └── archive.py        → ArchiveService
│
└── dependencies/         → Application Layer - DI Factories
    └── archive.py        → get_archive_repository(), get_archive_service()
```

### Layers (implicit):

| Folder | Layer | Responsibility |
|--------|-------|----------------|
| `entities/` | **Domain** | Pure business objects, generate their own identity |
| `interfaces/` | **Domain** | Contracts/abstractions (Protocols) |
| `services/` | **Application** | Business logic, orchestration |
| `repositories/` | **Infrastructure** | Data access, persistence |
| `models/` | **Infrastructure** | ORM models (SQLModel) |
| `dependencies/` | **Application** | Factories for DI |

### Applied principles:

#### 1. **Dependency Inversion Principle (DIP)**
```python
# Service depends on abstraction, not implementation
class ArchiveService:
    def __init__(self, repository: ArchiveRepositoryProtocol):  # ← Protocol
        self.repository = repository
```

#### 2. **Entities generate their identity (DDD)**
```python
class Archive(ArchiveData):
    id: str = Field(default_factory=lambda: str(ULID()))  # ← Auto-generated
    deleted_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))
```

#### 3. **Repository only persists**
```python
def create(self, archive_data: ArchiveData, deleted_by: str | None) -> Archive:
    archive = Archive(**archive_data.model_dump(), deleted_by=deleted_by)  # ← Entity creates itself
    model = ArchiveModel.model_validate(archive)  # ← Converts
    self.session.add(model)  # ← Persists
    return archive
```

---

## 🏛️ Domains Layer - DDD + Vertical Slicing + Clean

**Purpose**: Business domains separated by context.

**Pattern**: **Domain-Driven Design** with **Vertical Slicing** + **Clean Architecture** (implicit layers).

### Domain structure:

```
domains/
└── restaurants/              → Bounded Context
    ├── entities/             → Domain Layer - Business entities
    │   └── restaurant.py     → RestaurantData, Restaurant
    │
    ├── interfaces/           → Domain Layer - Contracts
    │   └── restaurant.py     → RestaurantRepositoryProtocol
    │
    ├── models/               → Infrastructure Layer - ORM
    │   └── restaurant.py     → RestaurantModel (SQLModel)
    │
    ├── repositories/         → Infrastructure Layer - Persistence
    │   └── restaurant.py     → RestaurantRepository
    │
    ├── schemas/              → Presentation Layer - API DTOs
    │   └── restaurant.py     → CreateRestaurantRequest, RestaurantResponse
    │
    ├── services/             → Application Layer - Business logic
    │   └── restaurant.py     → RestaurantService
    │
    ├── routes/               → Presentation Layer - Endpoints
    │   └── restaurant.py     → @router.get(), @router.post()
    │
    └── dependencies/         → Application Layer - DI Factories
        └── sql.py            → get_restaurant_repository()
```

### Features:

#### 1. **Vertical Slicing**
Each domain is independent and contains all its layers:
- ✅ `restaurants/` has everything needed for restaurants
- ✅ `users/` would have everything needed for users
- ✅ No cross-dependencies between domains

#### 2. **Clean Architecture (Layered - Implicit)**
Folders are not called "domain/", "application/", "infrastructure/", but the layers exist:

| Folder | Clean Layer | Depends on |
|--------|-------------|------------|
| `entities/` | Domain | Nothing (pure) |
| `interfaces/` | Domain | Nothing (abstract) |
| `schemas/` | Presentation | entities/ |
| `services/` | Application | interfaces/ |
| `repositories/` | Infrastructure | entities/, models/ |
| `models/` | Infrastructure | Nothing (ORM) |
| `routes/` | Presentation | services/, schemas/ |

#### 3. **Dependency rules**

```
routes/          → uses → services/, schemas/
    ↓
services/        → uses → interfaces/ (Protocols)
    ↓
repositories/    → implements → interfaces/
    ↓
models/          → maps → entities/
    ↓
entities/        → independent (core)
```

**Never**: Infrastructure → Domain ❌  
**Always**: Domain ← Infrastructure ✅

---

## 🔄 Request Flow

### Example: DELETE /restaurants/{id}

```
1. Route (Presentation Layer)
   ↓ receives HTTP request
   ↓ extracts: session via Depends()
   
2. Factory dependencies
   ↓ archive_repo = get_archive_repository(session)
   ↓ archive_service = get_archive_service(archive_repo)
   
3. Service (Application Layer)
   ↓ archive_service.archive_entity(table, entity, note, user_id)
   ↓ creates: Archive entity (with auto-generated ID)
   
4. Repository (Infrastructure Layer)
   ↓ converts: Archive → ArchiveModel
   ↓ persists: session.add(), session.commit()
   
5. Response
   ↓ returns: Archive entity
   ↓ serializes: Pydantic → JSON
   ↓ returns: HTTP response
```

---

## 📏 Conventions and Standards

### Naming

| Type | Pattern | Example |
|------|---------|---------|
| **Entities (without ID)** | `{Name}Data` | `ArchiveData`, `RestaurantData` |
| **Entities (with ID)** | `{Name}` | `Archive`, `Restaurant`, `Audit` |
| **Models (ORM)** | `{Name}Model` | `ArchiveModel`, `RestaurantModel` |
| **Protocols** | `{Name}Protocol` | `ArchiveRepositoryProtocol` |
| **Repositories** | `{Name}Repository` | `ArchiveRepository` |
| **Services** | `{Name}Service` | `ArchiveService` |
| **Schemas (request)** | `{Action}{Name}Request` | `CreateRestaurantRequest`, `UpdateRestaurantRequest` |
| **Schemas (response)** | `{Name}Response` | `RestaurantResponse` |

### Dependency Injection

**Only Routes use `Depends()`:**

```python
# ✅ Correct
@router.delete("/restaurants/{id}")
def delete_restaurant(
    session: Session = Depends(get_sqlite_session_dependency),  # ← Only here
):
    repo = get_archive_repository(session)      # ← Simple factory
    service = get_archive_service(repo)         # ← Simple factory
```

**Internal layers use constructors:**

```python
# ✅ Correct
def get_archive_service(repository: ArchiveRepositoryProtocol) -> ArchiveService:
    return ArchiveService(repository)  # ← Simple constructor
```

### Type Hints

- ✅ Use `Protocol` for abstractions
- ✅ Use native Python 3.12+ type hints (`list[str]`, `dict[str, any]`)
- ✅ Use `str | None` instead of `Optional[str]`

---

## 🎯 Applied SOLID Principles

### Single Responsibility
- Each class has a single responsibility
- `ArchiveService` → business logic
- `ArchiveRepository` → persistence

### Open/Closed
- Open for extension (new `Protocol` implementations)
- Closed for modification (interfaces don't change)

### Liskov Substitution
- Any implementation of `ArchiveRepositoryProtocol` is interchangeable

### Interface Segregation
- Small, specific Protocols
- `ArchiveRepositoryProtocol` only has `create()` (for now)

### Dependency Inversion
- **Services depend on Protocols (abstractions)**
- **Repositories implement Protocols**
- **Routes inject concrete implementations**

---

## 🧪 Testability

The architecture facilitates testing at each layer:

### Unit Tests (without DB)
```python
def test_archive_service():
    mock_repo = Mock(spec=ArchiveRepositoryProtocol)
    service = ArchiveService(mock_repo)  # ← Without DB
    
    # Test pure logic
    result = service.archive_entity(...)
```

### Integration Tests (with DB)
```python
def test_archive_repository():
    session = create_test_session()
    repo = ArchiveRepository(session)  # ← With real DB
    
    archive = repo.create(...)
    assert archive.id
```

### E2E Tests
```python
def test_delete_endpoint(client: TestClient):
    response = client.delete("/restaurants/123")
    assert response.status_code == 200
```

---

## 📚 Resources

### Applied patterns:
- **Hexagonal Architecture**: Alistair Cockburn
- **Clean Architecture**: Robert C. Martin (Uncle Bob)
- **Domain-Driven Design**: Eric Evans
- **Vertical Slice Architecture**: Jimmy Bogard

### Principles:
- **SOLID**: Robert C. Martin
- **Dependency Inversion Principle**: Key to Clean Architecture
- **Separation of Concerns**: Each layer with clear responsibility

---

## 🚀 Architecture Advantages

1. **Modularity**: Independent domains, easy to scale
2. **Testability**: Each layer is independently testable
3. **Maintainability**: Localized changes, low coupling
4. **Flexibility**: Easy to change implementations (DB, external services)
5. **Clarity**: Consistent structure, easy to understand
6. **DDD Compliant**: Entities have identity, repositories only persist
7. **SOLID Compliant**: All principles applied

---

## 📝 Conclusion

This hybrid architecture combines the best of multiple patterns:

- **Hexagonal** to isolate external dependencies
- **DDD + Vertical Slicing** to organize business domains
- **Clean Architecture** for separation of responsibilities

The result is a **maintainable**, **testable**, **scalable**, and **flexible** system.
