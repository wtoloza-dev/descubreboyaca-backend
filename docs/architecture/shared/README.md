# Shared Layer

## Purpose

The `app/shared/` layer contains **reusable code** that is used across **multiple domains** but doesn't belong to any specific domain. It provides common abstractions, utilities, and base classes to avoid code duplication.

## Philosophy

**Shared is the DRY (Don't Repeat Yourself) layer** - If code is used by 2+ domains, it should probably live here.

```
┌──────────────────────────────────────┐
│        Domain: Restaurants            │
│  ┌────────────────────────────────┐  │
│  │   Uses: Audit, Pagination,     │  │
│  │   BaseModel, GeoLocation       │  │
│  └────────────┬───────────────────┘  │
└───────────────┼──────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│           Shared Layer                │
│  • Base entities                      │
│  • Common exceptions                  │
│  • Value objects                      │
│  • Factories (ULID, datetime)         │
└──────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│        Domain: Reviews                │
│  Also uses shared components          │
└──────────────────────────────────────┘
```

## Structure

```
app/shared/
├── dependencies/           # Shared FastAPI dependencies
│   ├── pagination.py      # Pagination dependency
│   └── sql.py             # Database session dependency
│
├── domain/                # Domain primitives (DDD)
│   ├── constants/         # System-wide constants
│   │   └── audit.py       # Audit field constants
│   │
│   ├── entities/          # Base entity classes
│   │   ├── audit.py       # Audit mixin (created_at, updated_at, etc.)
│   │   ├── timestamp.py   # Timestamp mixin
│   │   └── user_tracking.py  # User tracking mixin
│   │
│   ├── enums/             # Shared enumerations
│   │   └── (none yet)
│   │
│   ├── exceptions/        # Base exception classes
│   │   ├── base.py        # DomainException
│   │   ├── not_found.py   # NotFoundException
│   │   ├── already_exists.py  # AlreadyExistsException
│   │   ├── unauthorized.py    # UnauthorizedException
│   │   ├── forbidden.py       # ForbiddenException
│   │   └── validation.py      # ValidationException
│   │
│   ├── factories/         # Factory functions
│   │   ├── id.py          # ULID generation
│   │   └── datetime.py    # UTC datetime helpers
│   │
│   ├── patterns/          # Design patterns
│   │   └── unit_of_work.py  # Unit of Work pattern
│   │
│   └── value_objects/     # Domain value objects
│       ├── pagination.py  # Pagination parameters
│       ├── geo_location.py    # Geographic coordinates
│       └── social_media.py    # Social media links
│
├── models/                # Base SQLModel classes
│   └── base.py            # Base database model
│
└── schemas/               # Base Pydantic schemas
    └── base.py            # Base API schema
```

## Key Components

### Base Entities

**Purpose**: Provide common fields that all entities need.

#### Audit Mixin

```python
# app/shared/domain/entities/audit.py

from datetime import datetime
from pydantic import BaseModel, Field
from app.shared.domain.factories import generate_ulid, utc_now

class Timestamp(BaseModel):
    """Base class with timestamp fields."""
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

class UserTracking(BaseModel):
    """Base class with user tracking fields."""
    created_by: str | None = None
    updated_by: str | None = None

class Audit(Timestamp, UserTracking):
    """Complete audit trail with identity.

    Provides:
        - id: ULID primary key
        - created_at: Creation timestamp
        - updated_at: Last update timestamp
        - created_by: Creator user ID
        - updated_by: Last updater user ID
    """
    id: str = Field(default_factory=generate_ulid)
```

**Usage**:
```python
# In domain entities
from app.shared.domain.entities import Audit

class Restaurant(RestaurantData, Audit):
    """Restaurant entity with automatic audit fields."""
    pass

# Automatically includes: id, created_at, updated_at, created_by, updated_by
```

### Base Exceptions

**Purpose**: Define exception hierarchy for consistent error handling.

```python
# app/shared/domain/exceptions/base.py

class DomainException(Exception):
    """Base exception for all domain errors."""

    def __init__(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        error_code: str | None = None,
    ):
        self.message = message
        self.context = context or {}
        self.error_code = error_code
        super().__init__(message)

# Specific exceptions inherit from base
class NotFoundException(DomainException):
    """Resource not found (404)."""
    pass

class AlreadyExistsException(DomainException):
    """Resource already exists (409)."""
    pass

class UnauthorizedException(DomainException):
    """Authentication required (401)."""
    pass

class ForbiddenException(DomainException):
    """Insufficient permissions (403)."""
    pass

class ValidationException(DomainException):
    """Validation error (400)."""
    pass
```

**Usage**:
```python
# Domain-specific exceptions inherit from shared base
from app.shared.domain.exceptions import NotFoundException

class RestaurantNotFoundException(NotFoundException):
    """Restaurant not found error."""

    def __init__(self, restaurant_id: str):
        super().__init__(
            message=f"Restaurant with ID '{restaurant_id}' not found",
            context={"restaurant_id": restaurant_id},
            error_code="RESTAURANT_NOT_FOUND",
        )
```

### Value Objects

**Purpose**: Represent domain concepts that don't have identity.

#### Pagination

```python
# app/shared/domain/value_objects/pagination.py

from pydantic import BaseModel, Field

class Pagination(BaseModel):
    """Pagination parameters for list queries."""
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        """Calculate SQL offset."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get SQL limit."""
        return self.page_size
```

#### GeoLocation

```python
# app/shared/domain/value_objects/geo_location.py

from decimal import Decimal
from pydantic import BaseModel, Field

class GeoLocation(BaseModel):
    """Geographic coordinates."""
    latitude: Decimal = Field(..., ge=-90, le=90)
    longitude: Decimal = Field(..., ge=-180, le=180)

    class Config:
        frozen = True  # Immutable
```

#### SocialMedia

```python
# app/shared/domain/value_objects/social_media.py

from pydantic import BaseModel, HttpUrl

class SocialMedia(BaseModel):
    """Social media profile links."""
    facebook: HttpUrl | None = None
    instagram: HttpUrl | None = None
    twitter: HttpUrl | None = None
    whatsapp: str | None = None

    class Config:
        frozen = True  # Immutable
```

### Factories

**Purpose**: Generate common values (IDs, timestamps).

#### ULID Factory

```python
# app/shared/domain/factories/id.py

from ulid import ULID

def generate_ulid() -> str:
    """Generate a ULID (Universally Unique Lexicographically Sortable ID).

    Returns:
        str: 26-character ULID string

    Example:
        >>> generate_ulid()
        '01JCXYZ123ABC456DEF789GHI0'
    """
    return str(ULID())
```

#### Datetime Factory

```python
# app/shared/domain/factories/datetime.py

from datetime import UTC, datetime

def utc_now() -> datetime:
    """Get current UTC datetime.

    Returns:
        datetime: Current time in UTC timezone

    Example:
        >>> utc_now()
        datetime(2025, 1, 19, 10, 30, 0, tzinfo=UTC)
    """
    return datetime.now(UTC)
```

### Dependencies

**Purpose**: Shared FastAPI dependency functions.

#### Session Dependency

```python
# app/shared/dependencies/sql.py

from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.clients.sql.dependencies import get_async_sql_client

async def get_async_session_dependency(
    client: Annotated[AsyncSQLClient, Depends(get_async_sql_client)],
) -> AsyncGenerator[AsyncSession, None]:
    """Get async database session.

    Yields:
        AsyncSession: Database session for the request

    Example:
        @router.get("/users")
        async def get_users(
            session: Annotated[AsyncSession, Depends(get_async_session_dependency)],
        ):
            # Use session
    """
    async with client.get_session() as session:
        yield session
```

#### Pagination Dependency

```python
# app/shared/dependencies/pagination.py

from fastapi import Query
from app.shared.domain.value_objects import Pagination

def get_pagination_dependency(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
) -> Pagination:
    """Get pagination parameters from query string.

    Args:
        page: Page number (starts at 1)
        page_size: Number of items per page (max 100)

    Returns:
        Pagination: Pagination value object

    Example:
        GET /restaurants?page=2&page_size=20
    """
    return Pagination(page=page, page_size=page_size)
```

## When to Add to Shared

### ✅ Add to shared when:
- Code is used by 2+ domains
- It's a cross-cutting concern (audit, pagination, errors)
- It's a domain primitive (value objects, base entities)
- It's a common pattern (Unit of Work, factories)
- It prevents duplication across domains

### ❌ Don't add to shared when:
- Code is domain-specific (belongs in domain layer)
- It's used by only one domain
- It contains business logic (belongs in application layer)
- It's framework-specific (might belong in core)

## Decision Flowchart

```
Is this code used by multiple domains?
    │
    ├─ No ──> Keep it in the domain layer
    │
    └─ Yes ──> Does it contain business logic?
               │
               ├─ Yes ──> Keep it in domain, consider extract to service
               │
               └─ No ──> Is it framework-independent?
                         │
                         ├─ Yes ──> Add to shared/domain
                         │
                         └─ No ──> Add to shared/dependencies or core
```

## Constants

**Purpose**: System-wide constant values.

```python
# app/shared/domain/constants/audit.py

AUDIT_FIELDS_EXCLUDE = {
    "created_at",
    "updated_at",
    "created_by",
    "updated_by",
}
"""Fields to exclude when comparing entities for changes."""
```

**Usage**:
```python
from app.shared.domain.constants import AUDIT_FIELDS_EXCLUDE

# Exclude audit fields when serializing
restaurant_dict = restaurant.model_dump(exclude=AUDIT_FIELDS_EXCLUDE)
```

## Design Patterns

### Unit of Work

```python
# app/shared/domain/patterns/unit_of_work.py

class UnitOfWork:
    """Unit of Work pattern for managing transactions.

    Example:
        async with UnitOfWork(session) as uow:
            await repository.create(entity)
            await other_repository.update(other_entity)
            # Both operations committed together
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        """Start transaction."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Commit or rollback transaction."""
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    async def commit(self):
        """Commit transaction."""
        await self.session.commit()

    async def rollback(self):
        """Rollback transaction."""
        await self.session.rollback()
```

## Benefits

| Benefit | Description |
|---------|-------------|
| **DRY** | Avoid code duplication across domains |
| **Consistency** | Common patterns used everywhere |
| **Maintainability** | Update once, affects all domains |
| **Type Safety** | Shared type definitions |
| **Discoverability** | Developers know where to find common code |

## Testing Strategy

### Unit Tests for Factories

```python
def test_generate_ulid():
    """Test ULID generation."""
    ulid1 = generate_ulid()
    ulid2 = generate_ulid()

    assert len(ulid1) == 26
    assert ulid1 != ulid2  # Unique

def test_utc_now():
    """Test UTC datetime generation."""
    now = utc_now()

    assert now.tzinfo == UTC
    assert now < datetime.now(UTC) + timedelta(seconds=1)
```

### Unit Tests for Value Objects

```python
def test_pagination_offset():
    """Test pagination offset calculation."""
    pagination = Pagination(page=3, page_size=10)

    assert pagination.offset == 20  # (3 - 1) * 10
    assert pagination.limit == 10

def test_geo_location_immutability():
    """Test GeoLocation is immutable."""
    location = GeoLocation(latitude=5.54, longitude=-73.36)

    with pytest.raises(ValidationError):
        location.latitude = 6.0  # Should fail (frozen)
```

## Dependencies

**This layer depends on**:
- Python standard library
- Pydantic (validation)
- SQLModel (base models)
- ulid-py (ULID generation)

**This layer is used by**:
- `app/domains/*` - All domain layers
- `app/core/*` - Core infrastructure
- `app/clients/*` - Client adapters

## Key Principles

1. **Domain-Agnostic** - Shared code knows nothing about specific domains
2. **Framework-Independent** - Avoid framework-specific code when possible
3. **Immutable Value Objects** - Value objects should be frozen
4. **Single Responsibility** - Each utility does one thing well
5. **Well-Documented** - Shared code should have excellent docs

## Common Patterns

### Using Audit Mixin

```python
# Every entity that needs audit trail
from app.shared.domain.entities import Audit

class MyEntity(MyEntityData, Audit):
    """Entity with automatic ID and timestamps."""
    pass
```

### Using Exceptions

```python
# Domain-specific exception inherits from shared
from app.shared.domain.exceptions import NotFoundException

class MyEntityNotFoundException(NotFoundException):
    def __init__(self, entity_id: str):
        super().__init__(
            message=f"Entity {entity_id} not found",
            error_code="MY_ENTITY_NOT_FOUND",
        )
```

### Using Pagination

```python
# In routes
from fastapi import Depends
from app.shared.dependencies import get_pagination_dependency

@router.get("/items")
async def list_items(
    pagination: Annotated[Pagination, Depends(get_pagination_dependency)],
):
    items = await repository.find_all(
        offset=pagination.offset,
        limit=pagination.limit,
    )
```

## Related Documentation

- [ARCHITECTURE.md - Section 5: Shared Components](../../ARCHITECTURE.md#5-shared-components)
- [domains.md](./domains.md) - How domains use shared components
- [core.md](./core.md) - Core infrastructure layer
- [clients.md](./clients.md) - Client adapters
