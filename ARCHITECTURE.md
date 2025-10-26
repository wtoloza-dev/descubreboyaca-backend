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
├── ports/              → Interfaces - Contracts
│   ├── sql.py          → SQLClientInterface
│   └── async_sql.py    → AsyncSQLClientInterface
    │
    ├── adapters/           → Concrete implementations
    │   ├── sqlite_client.py    → SQLiteClient, AsyncSQLiteClient
    │   └── postgres_client.py  → PostgreSQLClient, AsyncPostgreSQLClient
    │
    └── dependencies/       → Generic factories (app-agnostic)
        └── sqlite.py       → create_sqlite_client(), create_sqlite_session_dependency()

shared/
└── dependencies/
    └── sql.py              → App-specific factories with concrete config
                              get_sqlite_session_dependency() (uses settings)
```

### Principles:

- **Ports** (interfaces) define the contract
- **Adapters** (implementations) fulfill the contract
- The application depends on **Ports**, not **Adapters**
- Easy to swap implementations (SQLite ↔ PostgreSQL ↔ MySQL)
- **Clients are app-agnostic**: They accept configuration as parameters
- **Shared dependencies inject concrete config**: They use app settings and call client factories

### Example:

```python
# 1. Port (abstraction)
class SQLClientInterface(Protocol):
    def get_session(self) -> Generator[Session]: ...

# 2. Adapters (implementations)
class SQLiteClient:
    def __init__(self, database_url: str, echo: bool = False): ...
    def get_session(self) -> Generator[Session]: ...

class PostgreSQLClient:
    def __init__(self, database_url: str, echo: bool = False): ...
    def get_session(self) -> Generator[Session]: ...

# 3. Generic factories (app-agnostic) in clients/sql/dependencies/
def create_sqlite_client(database_url: str, echo: bool = False) -> SQLiteClient:
    """Generic factory - accepts all config as parameters."""
    return SQLiteClient(database_url=database_url, echo=echo)

# 4. App-specific factories in shared/dependencies/
def get_sqlite_session_dependency() -> Generator[Session, None, None]:
    """App-specific factory - injects concrete config from settings."""
    yield from create_sqlite_session_dependency(
        database_url="sqlite:///./test.db",  # ← Concrete config
        echo=settings.DEBUG,                  # ← From app settings
    )
```

This separation ensures that:
- `clients/` can be reused in any project (framework-agnostic)
- `shared/` contains the application-specific glue code
- Configuration is centralized in `settings`

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

**Pattern**: **Clean Architecture** with explicit `domain/` folder grouping all domain layer components.

### Structure:

```
shared/
├── domain/               → Domain Layer - Pure business logic
│   ├── entities/         → Business entities
│   │   ├── archive.py    → ArchiveData, Archive
│   │   └── audit.py      → Audit (base entity)
│   │
│   ├── interfaces/       → Contracts (Interfaces)
│   │   └── archive.py    → ArchiveRepositoryInterface
│   │
│   ├── value_objects/    → Immutable value objects
│   │   ├── geolocation.py → GeoLocation
│   │   ├── pagination.py  → PaginationParams
│   │   └── social_media.py → SocialMedia
│   │
│   ├── enums/            → Domain enumerations
│   └── constants/        → Domain constants
│
├── schemas/              → Presentation Layer - Shared DTOs
│   └── pagination.py     → PaginatedResponse[T] (generic)
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
    ├── archive.py        → get_archive_repository(), get_archive_service()
    ├── sql.py            → get_sqlite_session_dependency()
    └── pagination.py     → get_pagination_params()
```

### Layers (organized):

| Folder | Layer | Responsibility |
|--------|-------|----------------|
| `domain/entities/` | **Domain** | Pure business objects, generate their own identity |
| `domain/interfaces/` | **Domain** | Contracts/abstractions (Interfaces) |
| `domain/value_objects/` | **Domain** | Immutable value objects (GeoLocation, PaginationParams, SocialMedia) |
| `domain/enums/` | **Domain** | Domain enumerations |
| `domain/constants/` | **Domain** | Domain constants |
| `schemas/` | **Presentation** | API DTOs, shared response schemas |
| `services/` | **Application** | Business logic, orchestration |
| `repositories/` | **Infrastructure** | Data access, persistence |
| `models/` | **Infrastructure** | ORM models (SQLModel) |
| `dependencies/` | **Application** | Factories for DI |

### Applied principles:

#### 1. **Dependency Inversion Principle (DIP)**
```python
# Service depends on abstraction, not implementation
class ArchiveService:
    def __init__(self, repository: ArchiveRepositoryInterface):  # ← Interface
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
    ├── domain/               → Domain Layer - Pure business logic
    │   ├── entities/         → Business entities
    │   │   └── restaurant.py → RestaurantData, Restaurant
    │   │
    │   ├── interfaces/       → Contracts (Interfaces)
    │   │   └── restaurant.py → RestaurantRepositoryInterface
    │   │
    │   └── enums/            → Domain enumerations
    │       ├── cuisine_type.py → CuisineType
    │       ├── price_level.py  → PriceLevel
    │       └── restaurant_feature.py → RestaurantFeature
    │
    ├── models/               → Infrastructure Layer - ORM
    │   └── restaurant.py     → RestaurantModel (SQLModel)
    │
    ├── repositories/         → Infrastructure Layer - Persistence
    │   └── restaurant.py     → RestaurantRepository, AsyncRestaurantRepository
    │
    ├── schemas/              → Presentation Layer - API DTOs
    │   ├── create.py         → CreateRestaurantRequest, CreateRestaurantResponse
    │   ├── get.py            → GetRestaurantResponse
    │   └── list.py           → RestaurantListItem, ListRestaurantsResponse
    │
    ├── services/             → Application Layer - Business logic
    │   └── restaurant.py     → RestaurantService, AsyncRestaurantService
    │
    ├── routes/               → Presentation Layer - Endpoints
    │   ├── create.py         → POST /restaurants
    │   ├── get.py            → GET /restaurants/{id}
    │   └── list.py           → GET /restaurants
    │
    └── dependencies/         → Application Layer - DI Factories
        └── sql.py            → get_restaurant_service(), get_restaurant_repository()
```

### Features:

#### 1. **Vertical Slicing**
Each domain is independent and contains all its layers:
- ✅ `restaurants/` has everything needed for restaurants
- ✅ `users/` would have everything needed for users
- ✅ No cross-dependencies between domains

#### 2. **Clean Architecture (Layered - Explicit)**
Each domain has an explicit `domain/` folder containing all domain layer components:

| Folder | Clean Layer | Depends on |
|--------|-------------|------------|
| `domain/entities/` | Domain | Nothing (pure) |
| `domain/interfaces/` | Domain | Nothing (interfaces) |
| `domain/enums/` | Domain | Nothing (pure) |
| `domain/value_objects/` | Domain | Nothing (immutable) |
| `schemas/` | Presentation | domain/ |
| `services/` | Application | domain/interfaces/ |
| `repositories/` | Infrastructure | domain/, models/ |
| `models/` | Infrastructure | Nothing (ORM) |
| `routes/` | Presentation | services/, schemas/ |

#### 3. **Dependency rules**

```
routes/              → uses → services/, schemas/
    ↓
services/            → uses → domain/interfaces/ (Interfaces)
    ↓
repositories/        → implements → domain/interfaces/
    ↓
models/              → maps → domain/entities/
    ↓
domain/              → independent (core)
  ├── entities/      → pure business objects
  ├── interfaces/    → interface contracts
  ├── enums/         → enumerations
  ├── exceptions/    → domain exceptions
  └── value_objects/ → immutable objects
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

## 🔧 Service Layer Architecture

### Application Services vs Infrastructure Services

This architecture distinguishes between two types of services:

#### 1. **Application Services** (Business Logic / Orchestration)

**Purpose**: Orchestrate business use cases and coordinate domain operations.

**Naming**: `{Domain}Service`

**Characteristics**:
- ✅ Contain core business logic
- ✅ Orchestrate multiple dependencies (repositories, providers, clients)
- ✅ Define use cases (register user, login, transfer ownership)
- ✅ **Do NOT need abstraction** - they ARE the business logic
- ✅ Located in: `domains/{domain}/services/`

**Example**:
```python
# app/domains/auth/services/auth.py
class AuthService:
    """Orchestrates authentication use cases."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        token_provider: TokenProvider,
        password_hasher: PasswordHasher,
    ):
        self.user_repository = user_repository
        self.token_provider = token_provider
        self.password_hasher = password_hasher
    
    async def register(self, email: str, password: str) -> User:
        """Register a new user - Business use case."""
        # Hash password using infrastructure
        hashed = self.password_hasher.hash_password(password)
        # Save user using repository
        return await self.user_repository.create(...)
```

**When to use**: For orchestrating business logic and use cases.

---

#### 2. **Infrastructure Services** (Technical Details)

**Purpose**: Abstract external dependencies, libraries, and technical operations.

**Characteristics**:
- ✅ Wrap external libraries (bcrypt, JWT, OAuth SDKs)
- ✅ Provide technical operations (hashing, token generation, API calls)
- ✅ **ALWAYS need abstraction** (Protocol/Interface)
- ✅ Multiple implementations possible (bcrypt vs argon2, JWT vs Paseto)
- ✅ Located in: `domains/{domain}/services/` but abstracted in `domain/interfaces/`

**Naming Convention by Type**:

##### A) **Providers** - Create/Generate/Provide data or tokens

**Naming**: `{Technology}{What}Provider`

**When to use**: The service primarily creates, generates, or provides something.

**Example**:
```python
# Interface: app/domains/auth/domain/interfaces/token_provider.py
class TokenProvider(Protocol):
    """Interface for JWT token operations."""
    def create_access_token(self, user_id: str) -> str: ...
    def verify_token(self, token: str) -> dict: ...

# Implementation: app/domains/auth/services/token.py
class JWTTokenProvider:
    """JWT-based token provider."""
    def create_access_token(self, user_id: str) -> str:
        return jwt.encode({...}, self.secret_key)
```

**Other examples**: `ConfigProvider`, `IdentifierProvider`

---

##### B) **Hashers/Handlers** - Process/Transform/Validate data

**Naming**: `{Technology}{What}Hasher` or `{Technology}{What}Handler`

**When to use**: The service transforms, processes, or validates data.

**Example**:
```python
# Interface: app/domains/auth/domain/interfaces/password_hasher.py
class PasswordHasher(Protocol):
    """Interface for password hashing operations."""
    def hash_password(self, password: str) -> PasswordHash: ...
    def verify_password(self, plain: str, hashed: PasswordHash) -> bool: ...

# Implementation: app/domains/auth/services/password.py
class BcryptPasswordHasher:
    """Bcrypt-based password hasher."""
    def hash_password(self, password: str) -> PasswordHash:
        return bcrypt.hashpw(...)
```

**Other examples**: `FileHandler`, `ImageProcessor`, `EmailHandler`

---

##### C) **Clients** - Communicate with external systems

**Naming**: `{Provider}{What}Client`

**When to use**: The service communicates with external APIs or systems.

**Example**:
```python
# Interface: app/domains/auth/domain/interfaces/oauth_client.py
class OAuthClient(Protocol):
    """Interface for OAuth client operations."""
    def get_authorization_url(self) -> str: ...
    async def get_user_profile(self, code: str) -> OAuthProfile: ...

# Implementation: app/domains/auth/services/google_oauth.py
class GoogleOAuthClient:
    """Google OAuth client."""
    async def get_user_profile(self, code: str) -> OAuthProfile:
        # HTTP call to Google API
        response = await httpx.get("https://oauth2.googleapis.com/...")
        return OAuthProfile(...)
```

**Other examples**: `StripeClient`, `SendGridClient`, `SlackClient`

---

##### D) **Managers** - Manage state/lifecycle

**Naming**: `{What}Manager`

**When to use**: The service manages stateful resources or lifecycles.

**Example**:
```python
class SessionManager:
    """Manages user sessions and their lifecycle."""
    def create_session(self, user_id: str) -> Session:
        session = Session(...)
        self._sessions[session.id] = session
        return session
    
    def invalidate_session(self, session_id: str) -> None:
        del self._sessions[session_id]
```

**Other examples**: `ConnectionManager` (WebSockets), `CacheManager`, `TransactionManager`

---

### Decision Tree

```
Is it business logic that orchestrates use cases?
  └─ YES → {Domain}Service (no interface needed)
      └─ Example: AuthService, RestaurantService
  
  └─ NO → Infrastructure service (needs interface)
      
      What does it do?
      
      ├─ Creates/Generates/Provides something?
      │   └─ {Tech}{What}Provider
      │       └─ Example: JWTTokenProvider, ConfigProvider
      
      ├─ Transforms/Processes/Validates data?
      │   └─ {Tech}{What}Hasher or {Tech}{What}Handler
      │       └─ Example: BcryptPasswordHasher, ImageHandler
      
      ├─ Communicates with external API/system?
      │   └─ {Provider}{What}Client
      │       └─ Example: GoogleOAuthClient, StripeClient
      
      └─ Manages state/lifecycle?
          └─ {What}Manager
              └─ Example: SessionManager, CacheManager
```

---

### Summary Table

| Type | Purpose | Needs Interface? | Naming | Location |
|------|---------|------------------|--------|----------|
| **Application Service** | Business logic orchestration | ❌ No | `{Domain}Service` | `domains/{domain}/services/` |
| **Provider** | Create/generate/provide | ✅ Yes | `{Tech}{What}Provider` | `domains/{domain}/services/` + interface |
| **Hasher/Handler** | Transform/process | ✅ Yes | `{Tech}{What}Hasher` | `domains/{domain}/services/` + interface |
| **Client** | External communication | ✅ Yes | `{Provider}{What}Client` | `domains/{domain}/services/` + interface |
| **Manager** | State/lifecycle management | ✅ Yes | `{What}Manager` | `domains/{domain}/services/` + interface |

---

## 📏 Conventions and Standards

### Naming

| Type | Pattern | Example |
|------|---------|---------|
| **Entities (without ID)** | `{Name}Data` | `ArchiveData`, `RestaurantData` |
| **Entities (with ID)** | `{Name}` | `Archive`, `Restaurant`, `Audit` |
| **Models (ORM)** | `{Name}Model` | `ArchiveModel`, `RestaurantModel` |
| **Interfaces** | `{Name}Interface` or specific | `ArchiveRepositoryInterface`, `TokenProvider`, `PasswordHasher` |
| **Repositories** | `{Name}Repository` | `ArchiveRepository` |
| **Services (Application)** | `{Name}Service` | `ArchiveService`, `AuthService` |
| **Providers (Infrastructure)** | `{Tech}{Name}Provider` | `JWTTokenProvider` |
| **Hashers (Infrastructure)** | `{Tech}{Name}Hasher` | `BcryptPasswordHasher` |
| **Clients (Infrastructure)** | `{Provider}{Name}Client` | `GoogleOAuthClient` |
| **Schemas (request)** | `{Action}{Name}Request` | `CreateRestaurantRequest`, `UpdateRestaurantRequest` |
| **Schemas (response)** | `{Action}{Name}Response` | `CreateRestaurantResponse`, `GetRestaurantResponse` |
| **Schemas (list item)** | `{Name}ListItem` | `RestaurantListItem` |
| **Routes files** | `{action}.py` | `create.py`, `get.py`, `list.py` |
| **Route handlers** | `handle_{action}_{name}` | `handle_create_restaurant`, `handle_list_restaurants` |

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
def get_archive_service(repository: ArchiveRepositoryInterface) -> ArchiveService:
    return ArchiveService(repository)  # ← Simple constructor
```

### Type Hints

- ✅ Use `Protocol` for interface abstractions (named `*Interface`)
- ✅ Use native Python 3.12+ type hints (`list[str]`, `dict[str, Any]`)
- ✅ Use `str | None` instead of `Optional[str]`
- ✅ Use `class Generic[T]` syntax (Python 3.12+) instead of `TypeVar`

### API Patterns

#### Pagination
- **User-facing**: `page` (1-based) and `page_size` (1-100)
- **Database**: `offset` and `limit`
- **Conversion**: Handled by `get_pagination_params()` dependency
- **Response**: Standardized `PaginatedResponse[T]` generic schema

```python
# Dependency converts user params to DB params
def get_pagination_params(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> PaginationParams:
    offset = (page - 1) * page_size
    return PaginationParams(offset=offset, limit=page_size)

# Generic response schema
class PaginatedResponse[T](BaseModel):
    items: list[T]
    page: int
    page_size: int
    total: int

# Domain-specific usage
class ListRestaurantsResponse(PaginatedResponse[RestaurantListItem]):
    pass
```

#### Value Objects
- **Immutable**: Use `@dataclass(frozen=True)` or Pydantic `ConfigDict(frozen=True)`
- **Serialization**: Use `field_serializer` for custom JSON output
- **Validation**: Use `field_validator` for input validation
- **Examples**: `GeoLocation`, `SocialMedia`, `PaginationParams`

```python
# GeoLocation with precision control
@field_validator("latitude", "longitude", mode="before")
def validate_decimal(cls, v: Any) -> Decimal:
    return Decimal(str(v)).quantize(Decimal("0.00000001"))  # 8 decimals

@field_serializer("latitude", "longitude")
def serialize_decimal(self, value: Decimal) -> float:
    return round(float(value), 8)  # Clean JSON output
```

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
- Any implementation of `ArchiveRepositoryInterface` is interchangeable

### Interface Segregation
- Small, specific Interfaces
- `ArchiveRepositoryInterface` only has `create()` (for now)

### Dependency Inversion
- **Services depend on Interfaces (abstractions)**
- **Repositories implement Interfaces**
- **Routes inject concrete implementations**

---

## 🗄️ Database Migrations

### Pattern: Alembic with Manual Migrations

**Location**: `alembic/versions/`

### Structure:
```
alembic/
├── alembic.ini          → Configuration
├── env.py               → Environment setup (SQLModel integration)
├── script.py.mako       → Template for new migrations
└── versions/            → Migration files
    ├── 20251021_0918_xxx_create_archive_table.py
    └── 20251021_0918_xxx_create_restaurants_table.py
```

### Principles:
- ✅ **One table per migration**: Better control and rollback granularity
- ✅ **Manual migrations**: Explicit control over schema changes
- ✅ **Environment-aware**: Supports local (SQLite) and prod (PostgreSQL)
- ✅ **Bidirectional**: Both `upgrade()` and `downgrade()` implemented

### Migration Example:
```python
def upgrade() -> None:
    """Create restaurants table."""
    op.create_table(
        'restaurants',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        # ... more columns ...
        sa.PrimaryKeyConstraint('id', name=op.f('pk_restaurants')),
    )
    op.create_index(op.f('ix_restaurants_name'), 'restaurants', ['name'])

def downgrade() -> None:
    """Drop restaurants table."""
    op.drop_index(op.f('ix_restaurants_name'), table_name='restaurants')
    op.drop_table('restaurants')
```

### Workflow:
1. **Development**: `alembic revision -m "description"` → Create migration
2. **Apply**: `alembic upgrade head` → Run migrations
3. **Rollback**: `alembic downgrade -1` → Undo last migration
4. **Production**: `alembic upgrade head --sql > migration.sql` → Generate SQL for DBA

---

## 🧪 Testability

The architecture facilitates testing at each layer:

### Unit Tests (without DB)
```python
def test_archive_service():
    mock_repo = Mock(spec=ArchiveRepositoryInterface)
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
