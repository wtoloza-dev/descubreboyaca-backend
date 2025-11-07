# Architecture

This document provides a high-level overview of the Descubre Boyacá backend architecture. For detailed implementation patterns and guidelines, refer to the specific documentation files in `docs/code/`.

## 📐 Overview

The project uses a **hybrid architecture** that combines:

- **Hexagonal Architecture** (Ports & Adapters) for external communications
- **Domain-Driven Design (DDD)** with **Vertical Slicing** for business domains
- **Clean Architecture** (Layered) within each component

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

**Pattern**: **Ports & Adapters** - The application depends on abstractions (Ports), not concrete implementations (Adapters).

### Structure:

```
clients/
└── sql/
    ├── ports/                → Interfaces/Contracts (Ports)
    ├── adapters/             → Concrete implementations (Adapters)
    └── dependencies/         → Generic factories (app-agnostic)
```

### Key Principles:

- **Ports** (interfaces) define the contract
- **Adapters** (implementations) fulfill the contract
- Easy to swap implementations (SQLite ↔ PostgreSQL ↔ MySQL)
- **Clients are app-agnostic**: They accept configuration as parameters
- **Shared dependencies inject concrete config**: Located in `shared/dependencies/`

📖 **See**: `docs/code/Connection_Pool_Guide_ES.md`, `docs/code/Database_Best_Practices.md`

---

## ⚙️ Core Layer

**Purpose**: Global application configuration and lifecycle management.

```
core/
├── settings/         → Environment-specific configurations (local, staging, prod)
├── routes/           → Main route registration
├── lifespan.py       → Application lifecycle management
└── errors/           → Global error handling
```

📖 **See**: `docs/code/Lifespan_Explained_ES.md`, `docs/code/README_Lifespan.md`

---

## 🌐 Shared Layer - Clean Architecture

**Purpose**: Components shared across multiple domains following Clean Architecture principles.

### Structure:

```
shared/
├── domain/               → Domain Layer (Pure business logic)
│   ├── entities/         → Business entities
│   ├── interfaces/       → Contracts/abstractions
│   ├── value_objects/    → Immutable value objects
│   ├── enums/            → Domain enumerations
│   ├── constants/        → Domain constants
│   ├── exceptions/       → Domain exceptions
│   ├── factories/        → Entity factories
│   └── patterns/         → Domain patterns (e.g., Result)
│
├── schemas/              → Presentation Layer (API DTOs)
├── models/               → Infrastructure Layer (ORM)
├── repositories/         → Infrastructure Layer (Persistence)
├── services/             → Application Layer (Business logic)
└── dependencies/         → Application Layer (DI Factories)
```

### Clean Architecture Layers:

| Folder | Layer | Responsibility |
|--------|-------|----------------|
| `domain/` | Domain | Pure business logic (framework-agnostic) |
| `schemas/` | Presentation | API DTOs and response models |
| `services/` | Application | Business orchestration |
| `repositories/` | Infrastructure | Data access and persistence |
| `models/` | Infrastructure | ORM models (SQLModel) |
| `dependencies/` | Application | Dependency injection factories |

📖 **See**: `docs/code/Entities.md`, `docs/code/Value_Objects.md`, `docs/code/Enums.md`, `docs/code/Exceptions.md`

---

## 🏛️ Domains Layer - DDD + Vertical Slicing

**Purpose**: Business domains organized as independent **Bounded Contexts**.

**Pattern**: Each domain is a complete **vertical slice** containing all necessary layers.

### Domain Structure:

```
domains/
└── {domain}/             → Bounded Context (e.g., restaurants, auth, users)
    ├── domain/           → Domain Layer (Pure business logic)
    │   ├── entities/     → Domain entities
    │   ├── interfaces/   → Repository/service interfaces
    │   ├── enums/        → Domain-specific enums
    │   ├── value_objects/→ Domain value objects
    │   └── exceptions/   → Domain-specific exceptions
    │
    ├── models/           → Infrastructure Layer (ORM models)
    ├── repositories/     → Infrastructure Layer (Data access)
    ├── schemas/          → Presentation Layer (API DTOs)
    ├── services/         → Application Layer (Use cases)
    ├── routes/           → Presentation Layer (API endpoints)
    └── dependencies/     → Application Layer (DI factories)
```

### Vertical Slicing Benefits:

- ✅ Each domain is **self-contained** and **independent**
- ✅ No cross-dependencies between domains
- ✅ Easy to understand, test, and maintain
- ✅ Teams can work on different domains in parallel

### Dependency Rules:

```
routes/           → uses → services/, schemas/
    ↓
services/         → uses → domain/interfaces/ (abstractions)
    ↓
repositories/     → implements → domain/interfaces/
    ↓
models/           → maps to → domain/entities/
    ↓
domain/           → independent (pure business logic)
```

**Golden Rule**: **Infrastructure depends on Domain**, never the reverse.

📖 **See**: `docs/code/Routes.md`, `docs/code/Services.md`, `docs/code/Database_Repositories.md`, `docs/code/Models.md`, `docs/code/Schemas.md`

---

## 🔄 Request Flow

Example flow for a typical API request:

```
1. HTTP Request → Route (Presentation)
   ↓
2. Route extracts dependencies via Depends()
   ↓
3. Service (Application) orchestrates business logic
   ↓
4. Repository (Infrastructure) persists to database
   ↓
5. Entity (Domain) is returned
   ↓
6. Schema (Presentation) serializes to JSON
   ↓
7. HTTP Response
```

📖 **See**: `docs/code/Flujo_Visual_ES.md`

---

## 🔧 Service Layer Architecture

The architecture distinguishes between two types of services:

### 1. Application Services

**Purpose**: Orchestrate business use cases.

**Naming**: `{Domain}Service` (e.g., `AuthService`, `RestaurantService`)

**Characteristics**:
- ✅ Contain core business logic
- ✅ Orchestrate multiple dependencies
- ✅ **Do NOT need abstraction** (they ARE the business logic)

### 2. Infrastructure Services

**Purpose**: Abstract external dependencies and technical operations.

**Characteristics**:
- ✅ Wrap external libraries (bcrypt, JWT, OAuth)
- ✅ **ALWAYS need abstraction** (Protocol/Interface)
- ✅ Multiple implementations possible

**Types**:

| Type | Naming | Purpose | Example |
|------|--------|---------|---------|
| **Provider** | `{Tech}{What}Provider` | Create/generate/provide | `JWTTokenProvider` |
| **Hasher/Handler** | `{Tech}{What}Hasher` | Transform/process | `BcryptPasswordHasher` |
| **Client** | `{Provider}{What}Client` | External communication | `GoogleOAuthClient` |
| **Manager** | `{What}Manager` | State/lifecycle management | `SessionManager` |

📖 **See**: `docs/code/Services.md`

---

## 📏 Conventions and Standards

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| **Entities (without ID)** | `{Name}Data` | `RestaurantData` |
| **Entities (with ID)** | `{Name}` | `Restaurant` |
| **Models (ORM)** | `{Name}Model` | `RestaurantModel` |
| **Interfaces** | `{Name}Interface` | `RestaurantRepositoryInterface` |
| **Repositories** | `{Name}Repository` | `RestaurantRepository` |
| **Services** | `{Name}Service` | `RestaurantService` |
| **Schemas (request)** | `{Action}{Name}Request` | `CreateRestaurantRequest` |
| **Schemas (response)** | `{Action}{Name}Response` | `GetRestaurantResponse` |
| **Routes files** | `{action}.py` | `create.py`, `find_by_id.py` |

### Type Hints

- ✅ Use native Python 3.12+ type hints (`list[str]`, `dict[str, Any]`)
- ✅ Use `str | None` instead of `Optional[str]`
- ✅ Use `Protocol` for interface abstractions
- ✅ Use `class Generic[T]` syntax (Python 3.12+)

### Dependency Injection

- **Routes**: Use `Depends()` for dependency injection
- **Internal layers**: Use simple constructors and factory functions

```python
# ✅ In routes
@router.post("/restaurants")
def create_restaurant(
    session: Session = Depends(get_sqlite_session_dependency),
):
    repo = get_restaurant_repository(session)
    service = get_restaurant_service(repo)
```

📖 **See**: `docs/code/Dependencies.md`

---

## 🎯 SOLID Principles

| Principle | Application |
|-----------|-------------|
| **Single Responsibility** | Each class has one responsibility |
| **Open/Closed** | Open for extension, closed for modification |
| **Liskov Substitution** | Interface implementations are interchangeable |
| **Interface Segregation** | Small, specific interfaces |
| **Dependency Inversion** | Depend on abstractions, not concretions |

---

## 🗄️ Database

### Migrations

- **Tool**: Alembic
- **Strategy**: Manual migrations, one table per file
- **Environments**: SQLite (local), PostgreSQL (staging/prod)

📖 **See**: `docs/code/Database_Best_Practices.md`, `docs/code/Connection_Pool_Guide_ES.md`

### Repositories

- **Pattern**: Repository Pattern with interfaces
- **Sync & Async**: Both synchronous and asynchronous implementations

📖 **See**: `docs/code/Database_Repositories.md`, `docs/code/Repository_Interfaces.md`, `docs/code/API_Repositories.md`

---

## 🧪 Testability

The architecture facilitates testing at each layer:

- **Unit Tests**: Test services with mocked repositories (no DB)
- **Integration Tests**: Test repositories with real database
- **E2E Tests**: Test complete API flows

---

## 📚 Documentation

### Code Documentation

Located in `docs/code/`:

- **Architecture**: `Flujo_Visual_ES.md`, `Lifespan_Explained_ES.md`
- **Domain Layer**: `Entities.md`, `Value_Objects.md`, `Enums.md`, `Exceptions.md`
- **Infrastructure Layer**: `Models.md`, `Database_Repositories.md`, `Repository_Interfaces.md`
- **Application Layer**: `Services.md`, `Dependencies.md`
- **Presentation Layer**: `Routes.md`, `Schemas.md`
- **Database**: `Database_Best_Practices.md`, `Connection_Pool_Guide_ES.md`
- **Cheat Sheets**: `Cheat_Sheet_ES.md`, `Connection_Pool_Quick_Reference_ES.md`

---

## 🚀 Architecture Advantages

1. **Modularity**: Independent domains, easy to scale
2. **Testability**: Each layer is independently testable
3. **Maintainability**: Localized changes, low coupling
4. **Flexibility**: Easy to swap implementations
5. **Clarity**: Consistent structure, easy to understand
6. **DDD Compliant**: Entities have identity, repositories only persist
7. **SOLID Compliant**: All principles applied

---

## 📝 Summary

This architecture combines:

- **Hexagonal Architecture** → Isolate external dependencies
- **Domain-Driven Design** → Organize business domains
- **Vertical Slicing** → Self-contained domain modules
- **Clean Architecture** → Clear separation of concerns

The result is a **maintainable**, **testable**, **scalable**, and **flexible** system.

---

## 🔗 Quick Reference

| I want to... | See documentation |
|-------------|-------------------|
| Understand the overall flow | `docs/code/Flujo_Visual_ES.md` |
| Create a new entity | `docs/code/Entities.md` |
| Create a new repository | `docs/code/Database_Repositories.md` |
| Create a new service | `docs/code/Services.md` |
| Create a new route | `docs/code/Routes.md` |
| Understand database connections | `docs/code/Connection_Pool_Guide_ES.md` |
| Quick reference for common tasks | `docs/code/Cheat_Sheet_ES.md` |
