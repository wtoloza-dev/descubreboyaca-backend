# Database Models (ORM)

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Database Models** | `Infrastructure Layer` | `SQLModel` `ORM` `Database Persistence` |

## Definition

Models are SQLModel/SQLAlchemy classes that represent database tables and handle persistence. They act as the bridge between domain entities and the database, managing data serialization, type conversion, and database-specific concerns.

## Pattern

**Model = AuditModel + Business Fields + Database Metadata**

```
Business Fields + AuditModel (id, timestamps, user tracking, soft delete) = xxxModel
```

Models inherit audit capabilities and add domain-specific fields with database types.

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Filename | `{entity}_snake_case.py` | `prompt_version.py` |
| Model Class | `{Entity}Model` | `PromptVersionModel` |
| Table Name | `{entity}_snake_case` | `prompt_version` |

## Implementation Rules

### Model Structure
```python
class XxxModel(AuditModel, table=True):
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
- Always inherit from `AuditModel` with `table=True`
- Define `__tablename__` immediately after docstring
- Inherit id, timestamps, user tracking, and soft delete from `AuditModel`
- Only define business-specific fields in the model
- Use appropriate SQLAlchemy types when needed (`sa_type` parameter)

### AuditModel Inheritance

All models inherit these fields from `AuditModel`:

```python
# From ULIDMixin
id: str  # ULID identifier (primary key)

# From DatetimeMixin
created_at: datetime  # Creation timestamp
updated_at: datetime  # Last update timestamp

# From UserTrackingMixin
created_by: str  # User who created the record
updated_by: str  # User who last updated the record

# From SoftDeleteMixin
deleted_at: datetime | None  # Deletion timestamp
deleted_by: str | None  # User who deleted the record
is_deleted: bool  # Soft deletion flag
```

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
# ✅ CORRECT - Use ULIDType for ULID references
from app.shared.models.sqlalchemy import ULIDType

prompt_id: str = Field(sa_type=ULIDType, description="Reference to prompt")
```

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
class XxxModel(AuditModel, table=True):
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
- ✅ Import `AuditModel` from `app.shared.models`
- ✅ `table=True` parameter in class definition
- ✅ `__tablename__` definition
- ✅ Use `sa_type=ULIDType` for ULID foreign keys
- ✅ Use `sa_type=JSON` for dict/list fields
- ✅ Use `sa_type=Text` for large text content
- ✅ All fields have `description` parameter
- ✅ Don't use `sa_type` for basic types (int, bool, str→VARCHAR, datetime)

## Documentation Template

```python
"""[Entity name] model for database persistence."""

from typing import Any

from sqlalchemy import JSON, Text
from sqlmodel import Field

from app.shared.models import AuditModel
from app.shared.models.sqlalchemy import ULIDType


class XxxModel(AuditModel, table=True):
    """[Entity] model for database persistence.
    
    [One sentence explaining what it represents].
    
    Attributes:
        field1: Description of field1.
        field2: Description of field2.
        field3: Description of field3.
    """
    
    __tablename__ = "xxx"
    
    # Foreign keys (ULID references)
    parent_id: str = Field(sa_type=ULIDType, description="Reference to parent entity")
    
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
prompt_id: str = Field(
    sa_type=ULIDType,
    index=True,  # Often indexed for queries
    description="Reference to prompt"
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
| `str` | TEXT | Yes | `content: str = Field(sa_type=Text)` |
| `str` | BINARY(16) | Yes | `id: str = Field(sa_type=ULIDType)` |
| `int` | INTEGER | No | `count: int` |
| `bool` | BOOLEAN | No | `is_active: bool` |
| `datetime` | DATETIME | No | `created_at: datetime` |
| `dict[str, Any]` | JSON | Yes | `config: dict = Field(sa_type=JSON)` |

## Checklist

- [ ] Inherits from `AuditModel` with `table=True`
- [ ] Has `__tablename__` defined
- [ ] Has proper module and class docstrings
- [ ] All fields have `description` parameter
- [ ] Uses `sa_type=ULIDType` for ULID references
- [ ] Uses `sa_type=JSON` for dict/list fields
- [ ] Uses `sa_type=Text` for large text content
- [ ] Uses `default_factory=dict` for mutable defaults (dict/list)
- [ ] **Does NOT use** `sa_type` for basic types (int, bool, str→VARCHAR, datetime)
- [ ] Foreign keys are indexed when appropriate
- [ ] No redefinition of audit fields (id, timestamps, etc.)
- [ ] Exported in `__init__.py`

## Anti-Patterns (Avoid)

### ❌ Redefining Audit Fields
```python
# DON'T - AuditModel already provides these
class XxxModel(AuditModel, table=True):
    id: str = Field(...)  # ❌ Already in AuditModel
    created_at: datetime = Field(...)  # ❌ Already in AuditModel
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

### ❌ Not Using ULIDType for References
```python
# DON'T - Wrong type for ULID storage
prompt_id: str = Field(description="Prompt ID")  # ❌ No sa_type

# DO - Use ULIDType for proper ULID handling
prompt_id: str = Field(sa_type=ULIDType, description="Prompt ID")  # ✅
```

### ❌ Missing table=True
```python
# DON'T - Won't create database table
class XxxModel(AuditModel):  # ❌ Missing table=True
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

### Simple Model (PromptModel)
```python
class PromptModel(AuditModel, table=True):
    """Prompt model."""

    __tablename__ = "prompt"

    name: str = Field(default=..., description="Prompt name")
    description: str | None = Field(default=None, description="Prompt description")
    system_prompt: str | None = Field(default=None, description="System prompt")
    user_prompt: str | None = Field(default=None, description="User prompt")
    variables: dict[str, Any] = Field(
        default_factory=dict, sa_type=JSON, description="JSON variables"
    )
    current_version: str = Field(default="0.0.0", description="Current version")
```

### Model with Foreign Key (PromptVersionModel)
```python
class PromptVersionModel(AuditModel, table=True):
    """Prompt version model."""

    __tablename__ = "prompt_version"

    prompt_id: str = Field(sa_type=ULIDType, description="Prompt ID")
    comment: str | None = Field(default=None, description="Version Comment")
    system_prompt: str | None = Field(default=None, description="System prompt")
    variables: dict[str, Any] = Field(
        default_factory=dict,
        sa_type=JSON,
        description="JSON variables"
    )
    iteration: int = Field(default=0, description="Iteration")
```

### Model with Complex Constraints (PromptOwnershipModel)
```python
class PromptOwnershipModel(AuditModel, table=True):
    """Prompt ownership and access control model."""

    __tablename__ = "prompt_ownership"

    prompt_id: str = Field(
        sa_type=ULIDType,
        index=True,
        description="Reference to the prompt"
    )
    owner_type: str = Field(max_length=20, description="Type of owner")
    owner_id: str = Field(max_length=255, index=True, description="Owner ID")
    access_level: str = Field(max_length=20, description="Access level")
    is_primary: bool = Field(description="Is primary owner")

    __table_args__ = (
        Index(
            "idx_prompt_ownership_unique",
            "prompt_id",
            "owner_type",
            "owner_id",
            unique=True,
        ),
        Index("idx_prompt_ownership_owner", "owner_type", "owner_id"),
    )
```

## Integration with Domain Layer

Models serve as the persistence layer for domain entities:

```
Domain Entity ──(mapper)──> Database Model ──(SQLAlchemy)──> Database
     ↓                              ↓                            ↓
PromptVersion          PromptVersionModel              prompt_version (table)
```

- **Entities**: Business logic and domain rules (domain layer)
- **Models**: Data persistence and database mapping (infrastructure layer)
- **Repositories**: Handle conversion between entities and models

