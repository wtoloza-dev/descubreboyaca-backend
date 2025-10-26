# Naming Conventions & Project Structure

This document outlines the naming conventions and structural best practices for the CazaLost backend project.

---

## Table of Contents

- [General Principles](#general-principles)
- [File Naming](#file-naming)
- [Class Naming](#class-naming)
- [Function Naming](#function-naming)
- [Layer-Specific Conventions](#layer-specific-conventions)
- [Project Structure](#project-structure)
- [Examples](#examples)

---

## General Principles

1. **Consistency**: All naming follows a consistent pattern across the codebase
2. **Clarity**: Names should be descriptive and self-explanatory
3. **Context**: Folder structure provides context, avoid redundancy in names
4. **Singular**: Entity folders use singular form (`user/`, `issue/`, not `users/`, `issues/`)
5. **Matching**: Schema folders and files must match route folders and files exactly

---

## File Naming

### Convention: `snake_case`

All Python files follow `snake_case` naming:

```
✅ user_service.py
✅ issue_repository_mysql.py
✅ create_or_update.py

❌ UserService.py
❌ issueRepositoryMySQL.py
❌ CreateOrUpdate.py
```

### Folder Structure Pattern

Folders and files should mirror each other between `routes/` and `schemas/`:

```
routes/
  └── user/
      ├── get.py
      └── create_or_update.py

schemas/
  └── user/
      ├── get.py                    ← Must match route file
      └── create_or_update.py       ← Must match route file
```

**Rule**: If a route exists at `routes/{entity}/{operation}.py`, a corresponding schema must exist at `schemas/{entity}/{operation}.py`

---

## Class Naming

### Convention: `PascalCase`

All classes use `PascalCase`:

```python
✅ class UserService:
✅ class IssueRepositoryMySQL:
✅ class GetUserSchemaResponse:

❌ class user_service:
❌ class issueRepositoryMySQL:
❌ class get_user_schema_response:
```

### Layer-Specific Class Patterns

| Layer | Pattern | Example |
|-------|---------|---------|
| **Models** | `{Entity}Model` | `UserModel` |
| **Entities** | `{Entity}Data` / `{Entity}` | `UserData`, `User` |
| **Interfaces** | `{Entity}RepositoryInterface` or specific | `UserRepositoryInterface`, `TokenProvider` |
| **Repositories** | `{Entity}Repository{Tech}` | `UserRepositoryMySQL` |
| **Services (Application)** | `{Entity}Service` | `UserService`, `AuthService` |
| **Providers (Infrastructure)** | `{Tech}{What}Provider` | `JWTTokenProvider` |
| **Hashers (Infrastructure)** | `{Tech}{What}Hasher` | `BcryptPasswordHasher` |
| **Clients (Infrastructure)** | `{Provider}{What}Client` | `GoogleOAuthClient` |
| **Managers (Infrastructure)** | `{What}Manager` | `SessionManager` |
| **Exceptions** | `{Entity}Exception` | `UserNotFoundException` |
| **Enums** | `{Entity}{Property}` (StrEnum) | `UserSite`, `SearchStatus` |
| **Value Objects** | `{Concept}` | `FoundDetail` |
| **Schemas** | `{Operation}{Entity}Schema{Type}` | `GetUserSchemaResponse` |
| **Dependencies** | `get_{entity}_{type}_dependency` | `get_user_service_dependency` |

### Domain Layer Class Patterns

#### Entities
```python
✅ class UserData(BaseModel):      # Entity without audit fields
✅ class User(AuditBasic, UserData):  # Complete entity with audit

❌ class UserEntity(BaseModel):
❌ class UserDTO(BaseModel):
```

#### Enums
```python
✅ class UserSite(StrEnum):      # Entity + Property
✅ class SearchStatus(StrEnum):  # Entity + Property

❌ class Sites(StrEnum):
❌ class Status(StrEnum):
```

#### Value Objects
```python
✅ class FoundDetail(BaseModel):   # Descriptive concept name

❌ class FoundDetailVO(BaseModel):
❌ class FoundDetailValueObject(BaseModel):
```

#### Exceptions
```python
✅ class UserNotFoundException(DomainException):     # Entity + Specific error + Exception
✅ class NoActiveWarehouseException(DomainException): # Descriptive error + Exception

❌ class UserNotFound(DomainException):
❌ class NoActiveWarehouse(DomainException):
```

---

## Function Naming

### Convention: `snake_case`

All functions use `snake_case`:

```python
✅ def get_user_by_id(user_id: str):
✅ def create_or_update(data: UserData):

❌ def GetUserById(user_id: str):
❌ def CreateOrUpdate(data: UserData):
```

### Route Handlers: `handle_` Prefix

**All route handler functions MUST be prefixed with `handle_`**:

> ⚠️ **CRITICAL**: This is a mandatory convention. All API route handlers must start with `handle_` to distinguish them from service/repository methods.

```python
# ✅ Correct
@router.get("/")
async def handle_get_user(user_id: str) -> GetUserSchemaResponse:
    ...

@router.post("/")
async def handle_create_or_update_user(data: CreateOrUpdateUserSchemaRequest):
    ...

# ❌ Incorrect
@router.get("/")
async def get_user(user_id: str):
    ...
```

**Pattern**: `handle_{operation}_{entity}` or `handle_{operation}`

### Dependency Injection Functions: `get_*_dependency`

**All dependency injection functions must follow this pattern**:

```python
# ✅ Correct
def get_user_service_dependency(
    repository: Annotated[UserRepositoryInterface, Depends(get_user_repository_dependency)]
) -> UserService:
    return UserService(repository=repository)

def get_user_repository_dependency(
    session: Annotated[Session, Depends(get_mysql_session_dependency)]
) -> UserRepositoryMySQL:
    return UserRepositoryMySQL(session=session)

def get_current_user_dependency(
    email: Annotated[str, Depends(get_current_user_header_dependency)]
) -> CurrentUser:
    # Logic to fetch and return current user
    ...

# ❌ Incorrect
def user_service_dependency():        # Missing 'get_' prefix and '_dependency' suffix
    ...

def get_user_service():               # Missing '_dependency' suffix
    ...

def user_service():                   # Missing both
    ...
```

**Pattern**: `get_{entity}_{type}_dependency` or `get_{concept}_dependency`

---

## Layer-Specific Conventions

### 1. Models (Database Layer)

**Purpose**: SQLModel classes representing database tables

**File Pattern**: `{entity}.py`  
**Class Pattern**: `{Entity}Model`

```python
# File: models/user.py
class UserModel(SQLModel, table=True):
    __tablename__ = "user"
    id: str = Field(...)
    email: str = Field(...)
```

**Rules**:
- One model per file
- File name is singular entity name
- Class name is `{Entity}Model`
- Must inherit from `SQLModel` with `table=True`

---

### 2. Interfaces (Domain Layer - Protocols)

**Purpose**: Abstract interfaces defining repository contracts

**File Pattern**: `{entity}_repository.py`  
**Class Pattern**: `{Entity}RepositoryInterface`

```python
# File: domain/interfaces/user_repository.py
class UserRepositoryInterface(Protocol):
    def get_by_id(self, user_id: str) -> User | None:
        ...
    
    def create(self, user_data: UserData) -> User:
        ...
```

**Rules**:
- One interface per file
- File name is `{entity}_repository.py`
- Class name is `{Entity}RepositoryInterface`
- Must inherit from `Protocol`
- Methods use `...` as body

---

### 3. Repositories (Infrastructure Layer)

**Purpose**: Concrete implementations of repository interfaces

**File Pattern**: `{entity}_repository_{technology}.py`  
**Class Pattern**: `{Entity}Repository{Technology}`

```python
# File: repositories/user_repository_mysql.py
class UserRepositoryMySQL:
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def get_by_id(self, user_id: str) -> User | None:
        ...
```

**Rules**:
- One repository per file
- File name includes technology suffix (e.g., `_mysql`, `_bigquery`)
- Class name is `{Entity}Repository{Technology}`
- Must implement corresponding interface

**Special Cases**:
- Complex repositories can be folders: `issue_repository_bigquery/`
  - Main class in `repository.py`
  - Queries in `queries/` subfolder

---

### 4. Services (Application & Infrastructure Layers)

#### A) Application Services (Business Logic / Orchestration)

**Purpose**: Orchestrate business use cases and coordinate domain operations

**File Pattern**: `{entity}_service.py` or `{domain}.py`  
**Class Pattern**: `{Entity}Service`

```python
# File: services/auth.py
class AuthService:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        token_provider: TokenProvider,
        password_hasher: PasswordHasher,
    ) -> None:
        self.repository = repository
        self.token_provider = token_provider
        self.password_hasher = password_hasher
    
    async def register(self, email: str, password: str) -> User:
        # Business logic orchestration
        hashed = self.password_hasher.hash_password(password)
        return await self.repository.create(...)
```

**Rules**:
- One service per file
- File name is `{domain}.py` (e.g., `auth.py`, `restaurant.py`)
- Class name is `{Domain}Service` (e.g., `AuthService`)
- **Do NOT need interface** - they are the business logic
- Inject abstractions (interfaces) via constructor

---

#### B) Infrastructure Services (Technical Operations)

**Purpose**: Abstract external dependencies, libraries, and technical operations

**These ALWAYS need interfaces/protocols**

##### B.1) Providers - Create/Generate/Provide

**File Pattern**: `{what}.py`  
**Interface Pattern**: `{What}Provider`  
**Implementation Pattern**: `{Tech}{What}Provider`

```python
# File: domain/interfaces/token_provider.py
class TokenProvider(Protocol):
    def create_access_token(self, user_id: str) -> str: ...

# File: services/token.py
class JWTTokenProvider:
    def create_access_token(self, user_id: str) -> str:
        return jwt.encode({...})
```

---

##### B.2) Hashers/Handlers - Transform/Process

**File Pattern**: `{what}.py`  
**Interface Pattern**: `{What}Hasher` or `{What}Handler`  
**Implementation Pattern**: `{Tech}{What}Hasher`

```python
# File: domain/interfaces/password_hasher.py
class PasswordHasher(Protocol):
    def hash_password(self, password: str) -> PasswordHash: ...

# File: services/password.py
class BcryptPasswordHasher:
    def hash_password(self, password: str) -> PasswordHash:
        return bcrypt.hashpw(...)
```

---

##### B.3) Clients - External Communication

**File Pattern**: `{provider}_{what}.py`  
**Interface Pattern**: `{What}Client`  
**Implementation Pattern**: `{Provider}{What}Client`

```python
# File: domain/interfaces/oauth_client.py
class OAuthClient(Protocol):
    async def get_user_profile(self, code: str) -> OAuthProfile: ...

# File: services/google_oauth.py
class GoogleOAuthClient:
    async def get_user_profile(self, code: str) -> OAuthProfile:
        # HTTP call to external API
        response = await httpx.get(...)
        return OAuthProfile(...)
```

---

**Rules for Infrastructure Services**:
- One service per file
- **MUST have interface/protocol** in `domain/interfaces/`
- Implementation in `services/`
- Inject configuration via constructor
- Used by Application Services

---

### 5. Routes (Presentation Layer)

**Purpose**: FastAPI route handlers

**File Pattern**: `{entity}/{operation}.py`  
**Function Pattern**: `handle_{operation}_{entity}`

```python
# File: routes/user/get.py
@router.get("/{user_id}")
async def handle_get_user(
    user_id: str,
    user_service: Annotated[UserService, Depends(get_user_service_dependency)],
) -> GetUserSchemaResponse:
    """Get a user by ID."""
    user = user_service.get_user(user_id)
    if not user:
        raise UserNotFoundException(identifier=user_id)
    return GetUserSchemaResponse.model_validate(user)
```

**Rules**:
- Organize by entity in singular folders: `user/`, `issue/`, `search/`
- One operation per file
- File name describes the operation: `get.py`, `create_or_update.py`, `list.py`
- Handler functions prefixed with `handle_`
- Must return schema types
- Must have matching schema file

---

### 6. Entities (Domain Layer)

**Purpose**: Domain entities representing business concepts

**File Pattern**: `{entity}.py`  
**Class Pattern**: `{Entity}Data` (without audit) / `{Entity}` (with audit)

```python
# File: domain/entities/user.py
class UserData(BaseModel):
    """User entity without audit fields."""
    email: EmailStr
    site_id: UserSite
    warehouses: list[str]
    warehouse_active: str
    language: UserLanguage = UserLanguage.ES

class User(AuditBasic, UserData):
    """Complete user entity with audit fields (id, created_at, updated_at)."""
    pass
```

**Rules**:
- Base entity: `{Entity}Data` contains business fields only
- Full entity: `{Entity}` inherits from `AuditBasic` and `{Entity}Data`
- Use `BaseModel` from Pydantic
- Entities are immutable business objects

---

### 7. Exceptions (Domain Layer)

**Purpose**: Domain-specific exceptions

**File Pattern**: `{error_description}.py`  
**Class Pattern**: `{Specific}Exception`

```python
# File: domain/exceptions/user_not_found.py
class UserNotFoundException(DomainException):
    """Raised when a user is not found."""
    
    def __init__(self, identifier: str) -> None:
        super().__init__(
            error_code="USER_NOT_FOUND",
            message=f"User with identifier '{identifier}' was not found",
            context={"identifier": identifier},
        )
```

**Rules**:
- One exception per file
- File name describes the error: `user_not_found.py`, `no_active_warehouse.py`
- Class name: `{Specific}Exception`
- Must inherit from `DomainException`
- Include error code, message, and context

---

### 8. Enums (Domain Layer)

**Purpose**: Domain enumerated values

**File Pattern**: `{entity}_{property}.py`  
**Class Pattern**: `{Entity}{Property}`

```python
# File: domain/enums/user_site.py
from enum import StrEnum

class UserSite(StrEnum):
    """User site enumeration."""
    MLA = "MLA"  # Argentina
    MLB = "MLB"  # Brazil
    MLM = "MLM"  # Mexico
```

**Rules**:
- One enum per file
- File name: `{entity}_{property}.py` in snake_case
- Class name: `{Entity}{Property}` in PascalCase
- Inherit from `StrEnum` for string enums (Python 3.11+)
- Use `IntEnum` for integer enums

---

### 9. Value Objects (Domain Layer)

**Purpose**: Immutable domain values without identity

**File Pattern**: `{concept}.py`  
**Class Pattern**: `{Concept}`

```python
# File: domain/value_objects/found_detail.py
class FoundDetail(BaseModel):
    """Value object representing found item details."""
    quantity: int
    location: str
    timestamp: datetime
```

**Rules**:
- One value object per file
- File name describes the concept: `found_detail.py`
- Class name is the concept in PascalCase: `FoundDetail`
- Use `BaseModel` from Pydantic
- Should be immutable (no setters)

---

### 10. Dependencies (Dependency Injection)

**Purpose**: FastAPI dependency injection functions

**File Pattern**: `{entity}_dependencies.py`  
**Function Pattern**: `get_{entity}_{type}_dependency`

```python
# File: dependencies/user_dependencies.py
def get_user_repository_dependency(
    session: Annotated[Session, Depends(get_mysql_session_dependency)]
) -> UserRepositoryMySQL:
    """Provide user repository dependency."""
    return UserRepositoryMySQL(session=session)

def get_user_service_dependency(
    repository: Annotated[UserRepositoryInterface, Depends(get_user_repository_dependency)]
) -> UserService:
    """Provide user service dependency."""
    return UserService(repository=repository)

def get_current_user_dependency(
    email: Annotated[str, Depends(get_current_user_header_dependency)]
) -> CurrentUser:
    """Provide current authenticated user dependency."""
    # Fetch user logic here
    ...
```

**Rules**:
- Group related dependencies in `{entity}_dependencies.py`
- Function name: `get_{what}_dependency`
- Must be used with FastAPI's `Depends()`
- Return concrete implementations or processed data
- Chain dependencies using `Depends()` in parameters

---

### 11. Schemas (DTOs - Data Transfer Objects)

**Purpose**: Request/Response data validation

**File Pattern**: `{entity}/{operation}.py` (matches routes)  
**Class Pattern**: `{Operation}{Entity}Schema{Request|Response}`

```python
# File: schemas/user/get.py
class GetUserSchemaResponse(BaseModel):
    """Response schema for getting a user."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    site_id: UserSite = Field(..., description="User site")
```

**Rules**:
- **Must mirror route structure exactly**
- File name matches corresponding route file
- Class name pattern: `{Operation}{Entity}Schema{Type}`
- Suffix with `Request` or `Response`
- Include `model_config = ConfigDict(from_attributes=True)` when validating from domain entities
- One schema file can contain multiple related schemas (Request + Response)

**Schema Types**:
- `*SchemaRequest`: For request body/parameters
- `*SchemaResponse`: For response data
- `*ItemSchema`: For individual items in lists
- Generic paginated responses use `PaginatedResponse[T]` from `app.shared.schemas`

---

## Project Structure

```
app/
├── shared/                              # Shared/Common code
│   ├── dependencies/
│   ├── domain/
│   │   ├── entities/                    # Shared entities (Audit, etc.)
│   │   ├── exceptions/                  # Base exceptions
│   │   └── interfaces/
│   ├── models/                          # Shared SQLModels
│   └── schemas/                         # Generic schemas (PaginatedResponse[T])
│
├── core/                                # Infrastructure
│   ├── errors/                          # Exception handlers & mappers
│   ├── settings/                        # Configuration
│   └── traceability/
│
├── clients/                             # External adapters
│   ├── sql/
│   ├── bigquery/
│   ├── http/
│   └── logger/
│
└── domains/                             # Business domains
    └── {domain_name}/                   # e.g., caza_lost
        ├── domain/                      # Domain core (Clean Architecture)
        │   ├── entities/                # Domain entities (business objects)
        │   ├── enums/                   # Domain enums
        │   ├── exceptions/              # Domain-specific exceptions
        │   ├── interfaces/              # Repository interfaces (Protocols)
        │   └── value_objects/           # Value objects
        │
        ├── models/                      # Database models (SQLModel)
        ├── repositories/                # Repository implementations
        ├── services/                    # Business logic services
        ├── schemas/                     # DTOs (Request/Response)
        ├── routes/                      # API endpoints (Controllers)
        └── dependencies/                # Dependency injection
```

---

## Examples

### Complete Example: User Entity

#### 1. Model
```python
# File: models/user.py
class UserModel(SQLModel, table=True):
    __tablename__ = "user"
    id: str = Field(default_factory=lambda: str(ULID()), primary_key=True)
    email: str = Field(nullable=False, unique=True)
```

#### 2. Interface
```python
# File: domain/interfaces/user_repository.py
class UserRepositoryInterface(Protocol):
    def get_by_email(self, email: str) -> User | None:
        ...
```

#### 3. Repository
```python
# File: repositories/user_repository_mysql.py
class UserRepositoryMySQL:
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(UserModel.email == email)
        result = self.session.exec(statement)
        model = result.one_or_none()
        return User.model_validate(model) if model else None
```

#### 4. Service
```python
# File: services/user_service.py
class UserService:
    def __init__(self, repository: UserRepositoryInterface) -> None:
        self.repository = repository
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)
```

#### 5. Schema
```python
# File: schemas/user/get.py
class GetUserSchemaResponse(BaseModel):
    """Response schema for getting a user."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
```

#### 6. Route
```python
# File: routes/user/get.py
@router.get("/{email}")
async def handle_get_user(
    email: str,
    user_service: Annotated[UserService, Depends(get_user_service_dependency)],
) -> GetUserSchemaResponse:
    """Get a user by email."""
    user = user_service.get_user_by_email(email)
    if not user:
        raise UserNotFoundException(identifier=email)
    return GetUserSchemaResponse.model_validate(user)
```

---

## Checklist for New Features

When adding a new feature, ensure:

- [ ] **Singular naming**: Entity folders are singular (`user/`, not `users/`)
- [ ] **File naming**: All files use `snake_case`
- [ ] **Class naming**: All classes use `PascalCase` with appropriate suffix
- [ ] **Route handlers**: All route functions prefixed with `handle_`
- [ ] **Schema matching**: Schema files match route files exactly
- [ ] **Interface suffix**: All protocols end with `Interface`
- [ ] **Model suffix**: All SQLModel classes end with `Model`
- [ ] **Service suffix**: All service classes end with `Service`
- [ ] **Repository suffix**: All repositories end with `Repository{Tech}`
- [ ] **ConfigDict**: Schemas have `model_config = ConfigDict(from_attributes=True)` when validating entities

---

## Anti-Patterns (What NOT to Do)

### ❌ Incorrect File Naming
```
❌ UserService.py           # PascalCase file
❌ user-service.py          # Kebab-case
✅ user_service.py          # snake_case
```

### ❌ Plural Entity Folders
```
❌ routes/users/
❌ schemas/issues/
✅ routes/user/
✅ schemas/issue/
```

### ❌ Mismatched Routes and Schemas
```
❌ routes/user/get.py       ← Route exists
   schemas/user/read.py     ← Schema doesn't match
   
✅ routes/user/get.py       ← Route exists
   schemas/user/get.py      ← Schema matches
```

### ❌ Missing Prefixes/Suffixes
```python
❌ class User(SQLModel, table=True):          # Missing Model suffix
❌ class UserRepository(Protocol):            # Missing Interface suffix
❌ async def get_user():                      # Missing handle_ prefix

✅ class UserModel(SQLModel, table=True):
✅ class UserRepositoryInterface(Protocol):
✅ async def handle_get_user():
```

### ❌ Inconsistent Naming
```python
❌ class UserService:                         # Service suffix
   class IssueManager:                        # Manager suffix (inconsistent)
   
✅ class UserService:
   class IssueService:
```

---

## Quick Reference Table

| Layer | File Pattern | Class/Function Pattern | Example |
|-------|-------------|----------------------|---------|
| **Models** | `{entity}.py` | `{Entity}Model` | `user.py` → `UserModel` |
| **Entities** | `{entity}.py` | `{Entity}Data` / `{Entity}` | `user.py` → `UserData`, `User` |
| **Interfaces** | `{entity}_repository.py` or `{what}.py` | `{Entity}RepositoryInterface` or specific | `user_repository.py` → `UserRepositoryInterface`, `token_provider.py` → `TokenProvider` |
| **Repositories** | `{entity}_repository_{tech}.py` | `{Entity}Repository{Tech}` | `user_repository_mysql.py` → `UserRepositoryMySQL` |
| **Services (App)** | `{domain}.py` | `{Domain}Service` | `auth.py` → `AuthService` |
| **Providers (Infra)** | `{what}.py` | `{Tech}{What}Provider` | `token.py` → `JWTTokenProvider` |
| **Hashers (Infra)** | `{what}.py` | `{Tech}{What}Hasher` | `password.py` → `BcryptPasswordHasher` |
| **Clients (Infra)** | `{provider}_{what}.py` | `{Provider}{What}Client` | `google_oauth.py` → `GoogleOAuthClient` |
| **Exceptions** | `{error_description}.py` | `{Specific}Exception` | `user_not_found.py` → `UserNotFoundException` |
| **Enums** | `{entity}_{property}.py` | `{Entity}{Property}` (StrEnum/IntEnum) | `user_site.py` → `UserSite` |
| **Value Objects** | `{concept}.py` | `{Concept}` | `found_detail.py` → `FoundDetail` |
| **Dependencies** | `{entity}_dependencies.py` | `get_{what}_dependency` | `user_dependencies.py` → `get_user_service_dependency()` |
| **Routes** | `{entity}/{operation}.py` | `handle_{operation}` | `user/get.py` → `handle_get_user()` |
| **Schemas** | `{entity}/{operation}.py` | `{Operation}{Entity}Schema{Type}` | `user/get.py` → `GetUserSchemaResponse` |

---

## Version

- **Last Updated**: October 2025
- **Project**: CazaLost Backend
- **Architecture**: Clean Architecture + Domain-Driven Design (DDD)

---

**Remember**: Consistency is key. When in doubt, follow existing patterns in the codebase.

