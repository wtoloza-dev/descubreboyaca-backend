# Database Models (ORM)

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Database Models** | `Infrastructure Layer` | `SQLModel` `ORM` `Database Persistence` |

## Definition

Models are SQLModel/SQLAlchemy classes that represent database tables and handle persistence. They act as the bridge between domain entities and the database, managing data serialization, type conversion, and database-specific concerns.

**Important:** `SQLModel` inheritance is **required** for all models. It provides the ORM functionality that:
- Maps Python classes to database tables
- Handles database operations (CRUD)
- Provides type validation and serialization
- Integrates with SQLAlchemy and Pydantic

## Pattern

**Model = AuditMixin + SQLModel + Business Fields + Database Metadata**

```
Business Fields + AuditMixin (id, timestamps, user tracking) + SQLModel = xxxModel
```

Models inherit audit capabilities from mixins and add domain-specific fields with database types.

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Filename | `{entity}_snake_case.py` | `prompt_version.py` |
| Model Class | `{Entity}Model` | `PromptVersionModel` |
| Table Name | `{entity}_snake_case` | `prompt_version` |

## Implementation Rules

### Model Structure
```python
from sqlmodel import Field, SQLModel
from app.shared.models import AuditMixin

class XxxModel(AuditMixin, SQLModel, table=True):
    """Xxx model for database persistence.
    
    [One sentence explaining what it represents].
    
    Attributes:
        field1: Description.
        field2: Description.
    """
    
    __tablename__ = "xxx"
    
    field1: str = Field(description="Description")
    field2: int = Field(description="Description")
```

**Key Points:**
- Always inherit from `AuditMixin` (or `AuditBasicMixin`), `SQLModel`, with `table=True`
- `SQLModel` is required for ORM functionality - it's what makes the class a database table
- Define `__tablename__` immediately after docstring
- Inherit id, timestamps, and user tracking from `AuditMixin` (or just id+timestamps from `AuditBasicMixin`)
- Only define business-specific fields in the model
- Use appropriate SQLAlchemy types when needed (`sa_type` parameter)

### Audit Mixin Inheritance

Choose the appropriate mixin based on your needs:

#### **AuditMixin** (Full Audit Trail)
Use for core business entities that need complete audit tracking:

```python
# From ULIDMixin
id: str  # ULID identifier (primary key)

# From TimestampMixin
created_at: datetime  # Creation timestamp
updated_at: datetime  # Last update timestamp

# From UserTrackingMixin
created_by: str | None  # User who created the record
updated_by: str | None  # User who last updated the record
```

Examples: `UserModel`, `RestaurantModel`, `DishModel`

#### **AuditBasicMixin** (ID + Timestamps Only)
Use for user-generated content where user relationship is explicit via foreign key:

```python
# From ULIDMixin
id: str  # ULID identifier (primary key)

# From TimestampMixin
created_at: datetime  # Creation timestamp
updated_at: datetime  # Last update timestamp
```

Examples: `ReviewModel`, `FavoriteModel` (user tracked via `user_id` foreign key)

#### **Other Mixins** (Custom Combinations)
For special cases like junction tables:

```python
# TimestampMixin + UserTrackingMixin (no ULID, uses composite PK)
created_at: datetime
updated_at: datetime
created_by: str | None
updated_by: str | None
```

Examples: `RestaurantOwnerModel` (uses composite primary key: `restaurant_id` + `owner_id`)

**Never redefine these fields in your models.**

### Type Annotations & Database Types

#### When to Use sa_type

**Only use `sa_type` when:**
- ✅ Custom types: `ULIDType`, `Enum`, etc.
- ✅ JSON fields: `dict` or `list` → `sa_type=JSON`
- ✅ Large text: `str` → `sa_type=Text` (instead of VARCHAR)
- ✅ Specific column types that differ from Python type inference

**Don't use `sa_type` for:**
- ❌ `int` → automatically maps to INTEGER
- ❌ `bool` → automatically maps to BOOLEAN
- ❌ `str` → automatically maps to VARCHAR (unless you need TEXT)
- ❌ `datetime` → automatically maps to DATETIME
- ❌ `float` → automatically maps to FLOAT

#### Foreign Key References (ULID)
```python
# ✅ RECOMMENDED - Use max_length=26 for ULID references (human-readable in DB)
restaurant_id: str = Field(
    foreign_key="restaurants.id",
    max_length=26,
    index=True,
    description="Reference to restaurant"
)
```

**Why VARCHAR(26) instead of BINARY(16)?**

While BINARY(16) saves 10 bytes per ULID and offers slightly better index performance, VARCHAR(26) is preferred because:
- ✅ **Human-readable in database** - ULIDs appear as `01JBQZ8X9M...` not `0x0192E7A3...`
- ✅ **Easy debugging** - Can copy/paste ULIDs directly from logs to SQL queries
- ✅ **Better DX** - Works seamlessly with DB admin tools (TablePlus, pgAdmin, DataGrip)
- ✅ **No conversion needed** - Direct queries without UNHEX() or conversion functions
- ⚠️ **Space trade-off acceptable** - 10 bytes per record (~10MB per million records)

**Note:** `ULIDType` with binary storage is available but not recommended unless you have tens of millions of records where space/performance becomes critical.

#### JSON Fields
```python
# ✅ CORRECT - Use JSON type for dict/list fields
from sqlalchemy import JSON

variables: dict[str, Any] = Field(
    default_factory=dict, 
    sa_type=JSON, 
    description="JSON variables"
)

config: dict[str, Any] | None = Field(
    default=None,
    sa_type=JSON,
    description="Configuration"
)
```

#### Text Fields (Large Content)
```python
# ✅ CORRECT - Use Text for large text content
from sqlalchemy import Text

system_prompt: str = Field(
    sa_type=Text,
    description="System prompt content"
)
```

#### Numeric Fields
```python
# ✅ CORRECT - int automatically maps to INTEGER
token_count: int = Field(description="Token count")
iteration: int = Field(default=0, description="Iteration number")

# sa_type is NOT needed for int - it's automatically inferred
# Only specify sa_type for custom types, JSON, Text, etc.
```

#### String Fields
```python
# With max length constraint
name: str = Field(max_length=255, description="Name")

# Without constraint (default VARCHAR)
description: str = Field(description="Description")

# Optional strings
comment: str | None = Field(default=None, description="Comment")
```

#### Boolean Fields
```python
is_primary: bool = Field(description="Is primary owner")
is_active: bool = Field(default=True, description="Is active")
```

### Field Configuration

#### Required Fields
```python
# Required field (no default)
name: str = Field(description="Name")
name: str = Field(default=..., description="Name")  # Explicit required
```

#### Optional Fields
```python
# Optional with None default
description: str | None = Field(default=None, description="Description")
```

#### Fields with Defaults
```python
# Simple defaults
version: str = Field(default="0.0.0", description="Version")
is_active: bool = Field(default=True, description="Is active")

# Factory defaults (for mutable types)
variables: dict[str, Any] = Field(
    default_factory=dict,
    sa_type=JSON,
    description="Variables"
)
```

#### Indexed Fields
```python
# Simple index
prompt_id: str = Field(
    sa_type=ULIDType,
    index=True,
    description="Prompt ID"
)
```

### Advanced: Table Arguments

For complex constraints and indexes:

```python
from sqlalchemy import Index

class XxxModel(AuditModel, table=True):
    """Xxx model."""
    
    __tablename__ = "xxx"
    
    field1: str = Field(...)
    field2: str = Field(...)
    
    __table_args__ = (
        # Unique constraint
        Index(
            "idx_xxx_unique",
            "field1",
            "field2",
            unique=True,
        ),
        # Composite index
        Index("idx_xxx_composite", "field1", "field2"),
    )
```

### Class Structure Order (Standard)
```python
from sqlmodel import Field, SQLModel
from app.shared.models import AuditMixin

class XxxModel(AuditMixin, SQLModel, table=True):
    """Docstring with purpose and key attributes."""
    
    __tablename__ = "xxx"  # ← Always first
    
    # Then field definitions
    field1: str = Field(...)
    field2: int = Field(...)
    
    # Then __table_args__ (if any)
    __table_args__ = (...)
```

**Standard Order:**
1. Class docstring
2. `__tablename__` (immediately after docstring)
3. Field definitions (business fields only)
4. `__table_args__` (if needed for indexes/constraints)

### Required Elements
- ✅ Module docstring with "model for database persistence"
- ✅ Class docstring explaining purpose
- ✅ Import appropriate mixin (`AuditMixin`, `AuditBasicMixin`, etc.) from `app.shared.models`
- ✅ Import `SQLModel` from `sqlmodel`
- ✅ Multiple inheritance: `(AuditMixin, SQLModel, table=True)` or `(AuditBasicMixin, SQLModel, table=True)`
- ✅ `table=True` parameter in class definition
- ✅ `__tablename__` definition
- ✅ Use `max_length=26` with `foreign_key` for ULID references
- ✅ Use `sa_type=JSON` for dict/list fields
- ✅ Use `sa_type=Text` for large text content
- ✅ All fields have `description` parameter
- ✅ Don't use `sa_type` for basic types (int, bool, str→VARCHAR, datetime)

## Documentation Template

```python
"""[Entity name] model for database persistence."""

from typing import Any

from sqlalchemy import JSON, Text
from sqlmodel import Field, SQLModel

from app.shared.models import AuditMixin


class XxxModel(AuditMixin, SQLModel, table=True):
    """[Entity] model for database persistence.
    
    [One sentence explaining what it represents].
    
    Attributes:
        field1: Description of field1.
        field2: Description of field2.
        field3: Description of field3.
    """
    
    __tablename__ = "xxx"
    
    # Foreign keys (ULID references as VARCHAR(26) for readability)
    parent_id: str = Field(
        foreign_key="parent_table.id",
        max_length=26,
        index=True,
        description="Reference to parent entity"
    )
    
    # String fields
    name: str = Field(description="Name")
    description: str | None = Field(default=None, description="Description")
    
    # JSON fields
    variables: dict[str, Any] = Field(
        default_factory=dict,
        sa_type=JSON,
        description="Variables"
    )
    
    # Text fields (large content)
    content: str = Field(sa_type=Text, description="Large text content")
    
    # Numeric fields
    iteration: int = Field(default=0, description="Iteration number")
    
    # Boolean fields
    is_active: bool = Field(default=True, description="Is active")
```

## Common Patterns

### Reference to Parent Entity
```python
# Standard ULID foreign key (VARCHAR(26) for human-readability)
restaurant_id: str = Field(
    foreign_key="restaurants.id",
    max_length=26,
    index=True,  # Often indexed for queries
    description="Reference to restaurant"
)

# Without foreign key constraint (for polymorphic references)
entity_id: str = Field(
    max_length=26,
    index=True,
    description="ULID of the entity"
)
```

### Versioning Fields
```python
version: str = Field(description="Version (semver format)")
source_version: str | None = Field(default=None, description="Source version")
iteration: int = Field(default=0, description="Iteration number")
```

### Configuration/Metadata Storage
```python
# Use JSON for flexible configuration
config: dict[str, Any] = Field(
    default_factory=dict,
    sa_type=JSON,
    description="Configuration settings"
)

# Or nullable for optional config
metadata: dict[str, Any] | None = Field(
    default=None,
    sa_type=JSON,
    description="Optional metadata"
)
```

### Large Text Content (Prompts, Descriptions)
```python
system_prompt: str | None = Field(
    default=None,
    sa_type=Text,
    description="System prompt content"
)

user_prompt: str | None = Field(
    default=None,
    sa_type=Text,
    description="User prompt content"
)
```

### Snapshot Fields (for History/Audit)
```python
# Capture state at a point in time
variables_snapshot: dict[str, Any] | None = Field(
    default=None,
    sa_type=JSON,
    description="Variables snapshot at execution time"
)

llm_config_snapshot: dict[str, Any] | None = Field(
    default=None,
    sa_type=JSON,
    description="LLM configuration snapshot"
)
```

### Ownership/Access Control
```python
owner_type: str = Field(max_length=20, description="Owner type")
owner_id: str = Field(max_length=255, index=True, description="Owner ID")
access_level: str = Field(max_length=20, description="Access level")
is_primary: bool = Field(description="Is primary owner")
```

## Type Mapping Guide

| Python Type | SQLAlchemy Type | Needs sa_type? | Example |
|-------------|-----------------|----------------|---------|
| `str` | VARCHAR | No | `name: str` |
| `str` | VARCHAR(26) | No | `user_id: str = Field(max_length=26)` (ULID) |
| `str` | TEXT | Yes | `content: str = Field(sa_type=Text)` |
| `int` | INTEGER | No | `count: int` |
| `bool` | BOOLEAN | No | `is_active: bool` |
| `datetime` | DATETIME | No | `created_at: datetime` |
| `dict[str, Any]` | JSON | Yes | `config: dict = Field(sa_type=JSON)` |
| `list[str]` | JSON | Yes | `tags: list = Field(sa_type=JSON)` |

## Checklist

- [ ] Inherits from appropriate mixin (`AuditMixin`, `AuditBasicMixin`, etc.) + `SQLModel` with `table=True`
- [ ] Has `__tablename__` defined
- [ ] Has proper module and class docstrings
- [ ] All fields have `description` parameter
- [ ] Uses `max_length=26` for ULID references (foreign keys and regular fields)
- [ ] Uses `sa_type=JSON` for dict/list fields
- [ ] Uses `sa_type=Text` for large text content
- [ ] Uses `default_factory=dict` for mutable defaults (dict/list)
- [ ] **Does NOT use** `sa_type` for basic types (int, bool, str→VARCHAR, datetime)
- [ ] Foreign keys are indexed when appropriate
- [ ] No redefinition of audit fields (id, timestamps, user tracking)
- [ ] Exported in `__init__.py`

## Anti-Patterns (Avoid)

### ❌ Redefining Audit Fields
```python
# DON'T - AuditMixin already provides these
from sqlmodel import SQLModel
from app.shared.models import AuditMixin

class XxxModel(AuditMixin, SQLModel, table=True):
    id: str = Field(...)  # ❌ Already in AuditMixin
    created_at: datetime = Field(...)  # ❌ Already in AuditMixin
```

### ❌ Missing sa_type for JSON
```python
# DON'T - Will fail with dict/list types
variables: dict[str, Any] = Field(description="Variables")  # ❌ No sa_type

# DO - Specify JSON type
variables: dict[str, Any] = Field(sa_type=JSON, description="Variables")  # ✅
```

### ❌ Missing default_factory for Mutable Defaults
```python
# DON'T - Mutable default is shared across instances
variables: dict[str, Any] = Field(default={}, sa_type=JSON)  # ❌

# DO - Use factory for mutable types
variables: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)  # ✅
```

### ❌ Missing ULID Specifications
```python
# DON'T - Missing max_length for ULID field
prompt_id: str = Field(description="Prompt ID")  # ❌ No max_length

# DO - Specify max_length=26 for ULID references
prompt_id: str = Field(
    foreign_key="prompts.id",
    max_length=26,
    description="Prompt ID"
)  # ✅

# DO - For polymorphic references (no FK constraint)
entity_id: str = Field(
    max_length=26,
    index=True,
    description="ULID of the entity"
)  # ✅
```

### ❌ Missing table=True
```python
# DON'T - Won't create database table
from sqlmodel import SQLModel
from app.shared.models import AuditMixin

class XxxModel(AuditMixin, SQLModel):  # ❌ Missing table=True
    __tablename__ = "xxx"
```

### ❌ Using sa_type for Basic Types
```python
# DON'T - Unnecessary sa_type for int
from sqlalchemy import Integer
count: int = Field(sa_type=Integer, description="Count")  # ❌

# DO - Let SQLModel infer the type
count: int = Field(description="Count")  # ✅

# DON'T - Unnecessary sa_type for bool
from sqlalchemy import Boolean
is_active: bool = Field(sa_type=Boolean, description="Active")  # ❌

# DO - Automatic inference
is_active: bool = Field(description="Active")  # ✅
```

## Examples from Codebase

### Simple Model with AuditMixin (UserModel)
```python
from sqlmodel import Field, SQLModel
from app.shared.models import AuditMixin

class UserModel(AuditMixin, SQLModel, table=True):
    """User model for database persistence."""

    __tablename__ = "users"

    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User's email address",
    )
    full_name: str = Field(
        max_length=255,
        description="User's full name",
    )
    hashed_password: str | None = Field(
        default=None,
        max_length=255,
        description="Bcrypt hashed password (nullable for OAuth users)",
    )
    role: str = Field(
        default="user",
        max_length=50,
        description="User's role in the system",
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active",
    )
```

### Model with JSON Fields (RestaurantModel)
```python
from sqlalchemy import JSON
from sqlmodel import Field, SQLModel
from app.shared.models import AuditMixin

class RestaurantModel(AuditMixin, SQLModel, table=True):
    """Restaurant model for database persistence."""

    __tablename__ = "restaurants"

    name: str = Field(
        max_length=255,
        index=True,
        description="Restaurant name",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Restaurant description",
    )
    location: dict[str, float] | None = Field(
        default=None,
        sa_type=JSON,
        description="Geographic coordinates as JSON object",
    )
    establishment_types: list[str] = Field(
        default_factory=list,
        sa_type=JSON,
        description="Array of establishment types",
    )
```

### Model with AuditBasicMixin (FavoriteModel)
```python
from sqlalchemy import Index, UniqueConstraint
from sqlmodel import Field, SQLModel
from app.shared.models import AuditBasicMixin

class FavoriteModel(AuditBasicMixin, SQLModel, table=True):
    """Favorite model for database persistence."""

    __tablename__ = "favorites"

    user_id: str = Field(
        foreign_key="users.id",
        max_length=26,
        index=True,
        description="User who created the favorite",
    )
    entity_type: str = Field(
        max_length=50,
        index=True,
        description="Type of entity being favorited",
    )
    entity_id: str = Field(
        max_length=26,
        index=True,
        description="ULID of the favorited entity",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "entity_type",
            "entity_id",
            name="uq_favorites_user_entity",
        ),
        Index("ix_favorites_user_type", "user_id", "entity_type"),
    )
```

### Model with Composite Primary Key (RestaurantOwnerModel)
```python
from sqlmodel import Field, SQLModel
from app.shared.models import TimestampMixin, UserTrackingMixin

class RestaurantOwnerModel(TimestampMixin, UserTrackingMixin, SQLModel, table=True):
    """Restaurant ownership relationship model."""

    __tablename__ = "restaurant_owners"

    restaurant_id: str = Field(
        foreign_key="restaurants.id",
        primary_key=True,
        max_length=26,
        description="ULID of the restaurant",
    )
    owner_id: str = Field(
        foreign_key="users.id",
        primary_key=True,
        max_length=26,
        description="ULID of the owner/manager user",
    )
    role: str = Field(
        default="owner",
        max_length=50,
        description="Role in restaurant management",
    )
    is_primary: bool = Field(
        default=False,
        description="Whether this is the primary owner",
    )
```

## Integration with Domain Layer

Models serve as the persistence layer for domain entities:

```
Domain Entity ──(mapper)──> Database Model ──(SQLAlchemy)──> Database
     ↓                              ↓                            ↓
Restaurant            RestaurantModel              restaurants (table)
User                  UserModel                    users (table)
Dish                  DishModel                    dishes (table)
Review                ReviewModel                  reviews (table)
Favorite              FavoriteModel                favorites (table)
```

- **Entities**: Business logic and domain rules (domain layer)
- **Models**: Data persistence and database mapping (infrastructure layer)
- **Repositories**: Handle conversion between entities and models

## Mixin Selection Guide

Choose the right mixin based on your model's requirements:

| Use Case | Mixin | Provides | Example |
|----------|-------|----------|---------|
| Core business entities | `AuditMixin` | id + timestamps + user tracking | `UserModel`, `RestaurantModel`, `DishModel` |
| User-generated content (explicit FK) | `AuditBasicMixin` | id + timestamps only | `ReviewModel`, `FavoriteModel` |
| Junction tables with composite PK | `TimestampMixin + UserTrackingMixin` | timestamps + user tracking | `RestaurantOwnerModel` |
| Archival/logging | `ULIDMixin` | id only | `ArchiveModel` |

