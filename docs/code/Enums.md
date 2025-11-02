# Domain Enumerations (Enums)

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Enumerations** | `Domain Layer` | `DDD` `Type Safety` `Constants` |

## Definition

Enumerations (Enums) are immutable sets of named constants that represent a fixed collection of related values in the domain. They provide type safety, prevent invalid values, and make code self-documenting by explicitly defining all possible states or categories.

**Key Characteristics:**
- **Type-Safe Constants**: Only predefined values are allowed
- **Self-Documenting**: Names describe what each value means
- **Immutable**: Values cannot be changed after definition
- **Domain Concepts**: Represent business rules and states
- **Validation Built-In**: Invalid values are rejected at parse time

## Why Use Enums?

### ✅ Benefits

1. **Type Safety**: Catch invalid values at compile/parse time
```python
# With Enum - Caught immediately
status = ExecutionStatus.SUCESS  # ❌ AttributeError: SUCESS doesn't exist

# Without Enum - Runtime bugs
status = "SUCESS"  # ✅ Compiles, ❌ Breaks at runtime
```

2. **Self-Documenting Code**: Clear valid options
```python
# With Enum - Clear what's allowed
def process(status: ExecutionStatus): ...

# Without Enum - Unclear what strings are valid
def process(status: str): ...  # What values are valid?
```

3. **IDE Autocomplete**: Better developer experience
```python
status = ExecutionStatus.  # IDE shows: PENDING, SUCCESS, ERROR...
```

4. **Refactoring Safety**: Change propagates everywhere
```python
# Rename PENDING → IN_PROGRESS
# All usages update, or compiler/linter catches them
```

## Types of Enums

### 1. State Enums
Represent lifecycle states or status values.
- Workflow states, execution status, approval states
- Example: `PENDING`, `ACTIVE`, `COMPLETED`, `FAILED`

### 2. Category Enums
Represent types or categories of domain objects.
- Resource types, entity categories, version types
- Example: `MAJOR`, `MINOR`, `PATCH`

### 3. Role/Permission Enums
Represent roles, access levels, or permissions.
- User roles, access levels, ownership types
- Example: `ADMIN`, `EDITOR`, `VIEWER`

### 4. Type Discriminator Enums
Represent content types or format discriminators.
- Content types, message types, data formats
- Example: `TEXT`, `IMAGE`, `VIDEO`

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Directory | `domain/enums/` | `app/domains/prompt/domain/enums/` |
| Filename | `{concept}_snake_case.py` | `access_level.py`, `execution_status.py` |
| Class Name | `{Concept}PascalCase` | `AccessLevel`, `ExecutionStatus` |
| Enum Values | `UPPER_SNAKE_CASE` | `MAJOR`, `LLM_MODEL`, `IN_PROGRESS` |

## Implementation Rules

### Basic Structure

```python
"""[Concept] enumeration for [purpose]."""

from enum import StrEnum


class XxxEnum(StrEnum):
    """[Brief description of what this enum represents].

    [Optional: Detailed explanation of the domain concept].

    Attributes:
        VALUE1: Description of what this value means.
        VALUE2: Description of what this value means.
        VALUE3: Description of what this value means.
    """

    VALUE1 = "value1"
    VALUE2 = "value2"
    VALUE3 = "value3"
```

### Class Structure Order

1. **Module docstring** - Describe the concept and purpose
2. **Imports** - `from enum import StrEnum`
3. **Class definition** - Inherit from `StrEnum`
4. **Class docstring** - Comprehensive description with all attributes
5. **Enum values** - One per line, UPPER_SNAKE_CASE

### Inheritance: Always Use `StrEnum`

**Always inherit from `StrEnum`** (not `Enum`, `IntEnum`, etc.):

```python
from enum import StrEnum

class ExecutionStatus(StrEnum):  # ✅ Correct
    """Execution status enumeration."""
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
```

**Why `StrEnum`?**
- ✅ JSON serialization works automatically
- ✅ Database storage as strings (human-readable)
- ✅ String comparison works naturally
- ✅ API responses are clear
- ✅ Backwards compatible with string literals

```python
# StrEnum benefits
status = ExecutionStatus.SUCCESS
assert status == "SUCCESS"  # ✅ Works
json.dumps({"status": status})  # ✅ {"status": "SUCCESS"}
```

### Naming Conventions

#### Enum Class Names
- Use `PascalCase`
- Descriptive of what it represents
- Singular form (not plural)

```python
# ✅ CORRECT
class ExecutionStatus(StrEnum): ...
class AccessLevel(StrEnum): ...
class VersionType(StrEnum): ...

# ❌ INCORRECT
class ExecutionStatuses(StrEnum): ...  # Don't pluralize
class execution_status(StrEnum): ...   # Not snake_case
class Status(StrEnum): ...             # Too generic
```

#### Enum Value Names
- Use `UPPER_SNAKE_CASE`
- Clear and descriptive
- No abbreviations unless standard

```python
# ✅ CORRECT
class TestCaseType(StrEnum):
    VARIABLE = "VARIABLE"
    LLM_MODEL = "LLM-MODEL"
    LLM_CONFIG = "LLM-CONFIG"

# ❌ INCORRECT
class TestCaseType(StrEnum):
    var = "VARIABLE"           # Not UPPER_CASE
    Llm_Model = "LLM-MODEL"    # Mixed case
    LLMCFG = "LLM-CONFIG"      # Unclear abbreviation
```

#### Enum Value Strings
- Can match the name or be different
- Use formats appropriate for storage/API
- Be consistent within the enum

```python
# Pattern 1: Match the name (UPPER_CASE)
class ExecutionStatus(StrEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"

# Pattern 2: Different case for API/storage (lowercase)
class OwnerType(StrEnum):
    USER = "user"
    TEAM = "team"
    PUBLIC = "public"

# Pattern 3: Special characters for readability
class TestCaseType(StrEnum):
    LLM_MODEL = "LLM-MODEL"    # Hyphen in string value
    LLM_CONFIG = "LLM-CONFIG"
```

### Documentation Requirements

#### Module Docstring
```python
"""[Concept] enumeration for [purpose].

[Optional: Extended explanation of the domain concept this enum represents,
when to use it, and any important business rules].
"""
```

#### Class Docstring
Must include:
1. Brief one-line summary
2. Optional detailed explanation
3. **Attributes section** listing all enum values with descriptions

```python
class ExecutionStatus(StrEnum):
    """Execution status for test case execution items.

    Represents the lifecycle states of a test case execution:
    - QUEUED: Batch execution has been queued to work queue (initial response)
    - PENDING: Execution has been queued but not yet started (individual items)
    - SUCCESS: Execution completed successfully with results
    - ERROR: Execution failed with an error
    - COMPLETED: Overall batch execution completed (used in summaries)
    
    Attributes:
        QUEUED: Batch execution has been queued to work queue.
        PENDING: Individual execution item is queued but not started.
        SUCCESS: Execution completed successfully with results.
        ERROR: Execution failed with an error.
        COMPLETED: Overall batch execution completed.
    """

    QUEUED = "QUEUED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    COMPLETED = "COMPLETED"
```

## Documentation Templates

### Template 1: Simple State Enum

```python
"""[State] enumeration for [entity]."""

from enum import StrEnum


class XxxStatus(StrEnum):
    """Status states for [entity].

    Represents the lifecycle states of [entity description].

    Attributes:
        PENDING: Initial state, [description].
        ACTIVE: [Description of active state].
        COMPLETED: [Description of completed state].
        FAILED: [Description of failed state].
    """

    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
```

### Template 2: Category/Type Enum

```python
"""[Concept] type enumeration."""

from enum import StrEnum


class XxxType(StrEnum):
    """Types of [concept].

    Defines the different categories/types of [entity].

    Attributes:
        TYPE1: [Description of what this type represents].
        TYPE2: [Description of what this type represents].
        TYPE3: [Description of what this type represents].
    """

    TYPE1 = "TYPE1"
    TYPE2 = "TYPE2"
    TYPE3 = "TYPE3"
```

### Template 3: Access/Role Enum

```python
"""[Access/Role] level enumeration."""

from enum import StrEnum


class XxxLevel(StrEnum):
    """Access levels for [resource].

    Defines permission levels for accessing and modifying [resource].

    Attributes:
        ADMIN: Full control including [specific permissions].
        EDITOR: Can modify but not [specific restrictions].
        VIEWER: Read-only access.
    """

    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
```

### Template 4: Versioning Enum

```python
"""[Versioning concept] enumeration."""

from enum import StrEnum


class VersionType(StrEnum):
    """Version type for semantic version increments.

    Follows semantic versioning principles (MAJOR.MINOR.PATCH).

    Attributes:
        MAJOR: Major version increment (X.0.0) - Breaking changes.
        MINOR: Minor version increment (x.Y.0) - New features, backwards compatible.
        PATCH: Patch version increment (x.y.Z) - Bug fixes, backwards compatible.
    """

    MAJOR = "MAJOR"
    MINOR = "MINOR"
    PATCH = "PATCH"
```

## Usage Examples

### Example 1: State Enum in Entity

```python
class ExecutionStatus(StrEnum):
    """Execution status for items."""
    
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

# Using in entity
class ExecutionItem(BaseModel):
    id: str
    status: ExecutionStatus  # ✅ Type-safe field
    
# Creating and validating
item = ExecutionItem(id="123", status=ExecutionStatus.PENDING)
item = ExecutionItem(id="123", status="PENDING")  # ✅ Auto-converted

# Type-safe comparison
if item.status == ExecutionStatus.SUCCESS:
    process_results(item)
```

### Example 2: Category Enum with Pattern Matching

```python
class ResourceType(StrEnum):
    """Resource type categories."""
    
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"

# Pattern matching
def process_resource(resource_type: ResourceType, data: dict):
    match resource_type:
        case ResourceType.TEXT:
            validate_text(data)
        case ResourceType.IMAGE:
            validate_image(data)
        case ResourceType.VIDEO:
            validate_video(data)
```

### Example 3: Permission Enum with Groups

```python
class AccessLevel(StrEnum):
    """Access permission levels."""
    
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

# Permission groups
WRITE_ACCESS = {AccessLevel.ADMIN, AccessLevel.EDITOR}

def can_modify(user_access: AccessLevel) -> bool:
    return user_access in WRITE_ACCESS
```

## Package Structure

### `__init__.py` Structure

Always export enums in the package's `__init__.py`:

```python
"""[Domain] enums package."""

from app.domains.xxx.domain.enums.status import XxxStatus
from app.domains.xxx.domain.enums.type import XxxType

__all__ = [
    "XxxStatus",
    "XxxType",
]
```

### Directory Structure

```
app/domains/{domain}/
├── domain/
│   ├── enums/
│   │   ├── __init__.py          # Export all enums
│   │   ├── status.py            # State enum
│   │   ├── type.py              # Category enum
│   │   └── access_level.py      # Permission enum
│   ├── entities/
│   ├── value_objects/
│   └── interfaces/
```

## Common Patterns

### Pattern 1: State Machine Enums

Use enums to define valid state transitions:

```python
class OrderStatus(StrEnum):
    """Order processing status."""
    
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# Define valid transitions
VALID_TRANSITIONS = {
    OrderStatus.DRAFT: {OrderStatus.SUBMITTED, OrderStatus.CANCELLED},
    OrderStatus.SUBMITTED: {OrderStatus.PROCESSING, OrderStatus.CANCELLED},
    OrderStatus.PROCESSING: {OrderStatus.COMPLETED, OrderStatus.CANCELLED},
    OrderStatus.COMPLETED: set(),  # Terminal state
    OrderStatus.CANCELLED: set(),  # Terminal state
}

def can_transition(from_status: OrderStatus, to_status: OrderStatus) -> bool:
    """Check if transition is valid."""
    return to_status in VALID_TRANSITIONS[from_status]
```

### Pattern 2: Enum Groups

Group related enum values for validation or filtering:

```python
class AccessLevel(StrEnum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

# Define permission groups
WRITE_ACCESS = {AccessLevel.OWNER, AccessLevel.ADMIN, AccessLevel.EDITOR}
ADMIN_ACCESS = {AccessLevel.OWNER, AccessLevel.ADMIN}

def can_write(access: AccessLevel) -> bool:
    return access in WRITE_ACCESS

def can_admin(access: AccessLevel) -> bool:
    return access in ADMIN_ACCESS
```

### Pattern 3: Enum with Metadata

Attach metadata to enum values using dictionaries:

```python
class VersionType(StrEnum):
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    PATCH = "PATCH"

# Metadata about each version type
VERSION_METADATA = {
    VersionType.MAJOR: {
        "resets": ["minor", "patch"],
        "significance": "Breaking changes",
    },
    VersionType.MINOR: {
        "resets": ["patch"],
        "significance": "New features, backwards compatible",
    },
    VersionType.PATCH: {
        "resets": [],
        "significance": "Bug fixes",
    },
}

def get_significance(version_type: VersionType) -> str:
    return VERSION_METADATA[version_type]["significance"]
```

### Pattern 4: Default Values

Use enums to provide clear default values:

```python
class ExecutionStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"

class ExecutionItem(BaseModel):
    """Execution item with default status."""
    
    test_case_id: str
    status: ExecutionStatus = ExecutionStatus.PENDING  # ✅ Clear default
```

## Integration with Pydantic

### Automatic Validation

```python
from pydantic import BaseModel

class Resource(BaseModel):
    type: ResourceType  # ✅ Validates automatically
    
# Valid values
resource = Resource(type=ResourceType.TEXT)  # ✅ Direct enum
resource = Resource(type="TEXT")  # ✅ String coerced to enum

# Invalid values
resource = Resource(type="INVALID")  # ❌ ValidationError
```

### JSON Serialization

```python
resource = Resource(type=ResourceType.TEXT)

# Serialization
json_data = resource.model_dump()  # {"type": "TEXT"}
json_str = resource.model_dump_json()  # '{"type":"TEXT"}'

# Deserialization
resource2 = Resource.model_validate_json(json_str)  # ✅ Works
```

### Optional Enums

```python
class Config(BaseModel):
    status: ResourceStatus | None = None  # Optional enum
    
config = Config()  # ✅ status is None
config = Config(status=ResourceStatus.ACTIVE)  # ✅
config = Config(status="ACTIVE")  # ✅ Auto-coerced
```

## API Integration

### FastAPI Path/Query Parameters

```python

from typing import Annotated

from fastapi import APIRouter, Query

@router.get("/resources")
async def list_resources(
    status: Annotated[ResourceStatus | None, Query()] = None
):
    """OpenAPI will show enum options in dropdown."""
    ...

# Valid: GET /resources?status=ACTIVE  ✅
# Invalid: GET /resources?status=INVALID  ❌ 422 Validation Error
```

### Request/Response Schemas

```python
class CreateResourceRequest(BaseModel):
    """Request schema with enum."""
    
    name: str
    type: ResourceType  # ✅ Enum in request
    
class ResourceResponse(BaseModel):
    """Response schema with enum."""
    
    id: str
    type: ResourceType  # ✅ Enum in response
    status: ResourceStatus

# OpenAPI automatically shows all valid enum values
```

## Required Elements Checklist

- [ ] Module docstring describing the enum purpose
- [ ] Class inherits from `StrEnum` (not `Enum` or `IntEnum`)
- [ ] Class has comprehensive docstring with Attributes section
- [ ] All enum values use `UPPER_SNAKE_CASE` naming
- [ ] String values are consistent (all upper, all lower, or special format)
- [ ] Each enum value documented in Attributes section
- [ ] Exported in `__init__.py`
- [ ] One enum per file (single responsibility)

## Anti-Patterns to Avoid

### ❌ Wrong Enum Type

```python
# BAD - Don't use plain Enum
from enum import Enum

class Status(Enum):  # ❌ Use StrEnum instead
    PENDING = "PENDING"
    
# BAD - Don't use IntEnum for string values
from enum import IntEnum

class Status(IntEnum):  # ❌ Not for string values
    PENDING = 1
    SUCCESS = 2
```

### ❌ Inconsistent Value Format

```python
# BAD - Mixed formats
class Status(StrEnum):
    PENDING = "pending"      # lowercase
    SUCCESS = "SUCCESS"      # UPPERCASE
    InProgress = "in-progress"  # Mixed case
    
# GOOD - Consistent format
class Status(StrEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    IN_PROGRESS = "IN_PROGRESS"
```

### ❌ Too Generic Names

```python
# BAD - Too generic
class Type(StrEnum):  # ❌ What type?
    A = "A"
    B = "B"

# GOOD - Specific and clear
class TestCaseType(StrEnum):  # ✅ Clear context
    VARIABLE = "VARIABLE"
    LLM_MODEL = "LLM-MODEL"
```

### ❌ Missing Documentation

```python
# BAD - No docstrings
class Status(StrEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    
# GOOD - Full documentation
class ExecutionStatus(StrEnum):
    """Execution status for test cases.
    
    Attributes:
        PENDING: Execution queued but not started.
        SUCCESS: Execution completed successfully.
    """
    
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
```

### ❌ Magic Strings in Code

```python
# BAD - Magic strings
if status == "PENDING":  # ❌ Typo-prone, no type safety
    ...

# GOOD - Use enum
if status == ExecutionStatus.PENDING:  # ✅ Type-safe
    ...
```

### ❌ Mutable Enum (Using Variables)

```python
# BAD - Not an enum, just constants
PENDING = "PENDING"
SUCCESS = "SUCCESS"

# Can be accidentally changed
PENDING = "MODIFIED"  # ❌ Mutable

# GOOD - Real enum
class ExecutionStatus(StrEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    
# Cannot be changed
ExecutionStatus.PENDING = "MODIFIED"  # ❌ AttributeError
```

### ❌ Multiple Enums in One File

```python
# BAD - Multiple enums in one file
class Status(StrEnum):
    ...

class Type(StrEnum):
    ...
    
class Level(StrEnum):
    ...

# GOOD - One enum per file
# status.py
class Status(StrEnum):
    ...
```

## Best Practices

1. **Use `StrEnum` always**: Better JSON/API integration
2. **One enum per file**: Keeps code organized
3. **Clear, descriptive names**: Enum name and values should be self-documenting
4. **Consistent value format**: All uppercase, all lowercase, or consistent pattern
5. **Comprehensive docstrings**: Document what each value means
6. **Export in `__init__.py`**: Easy imports for consumers
7. **Use in type hints**: Leverage type safety everywhere
8. **Avoid magic strings**: Always use enum values in code
9. **Group related values**: If you have >7 values, consider splitting
10. **Document state transitions**: If enum represents states, document valid transitions

## When to Use Enums

✅ **Use Enums for:**
- Fixed set of related values (statuses, types, roles)
- Values that are part of domain language
- Values that need type safety
- Configuration options with limited choices
- State machine states
- Permission/access levels
- Message types or formats
- Versioning strategies

❌ **Don't Use Enums for:**
- Dynamic values from database
- User-generated content
- Values that change frequently
- Large sets of values (>20 items)
- Values with complex hierarchies → Use class hierarchies
- Binary flags → Use boolean fields
- Numeric ranges → Use int with validation

## Testing Enums

```python
def test_enum_values():
    """Test enum has expected values."""
    assert ResourceStatus.ACTIVE == "ACTIVE"
    
def test_enum_membership():
    """Test value is valid enum member."""
    assert "ACTIVE" in ResourceStatus.__members__.values()
    
def test_pydantic_validation():
    """Test enum validation in Pydantic models."""
    # Valid enum value
    resource = Resource(status=ResourceStatus.ACTIVE)
    assert resource.status == ResourceStatus.ACTIVE
    
    # Valid string coercion
    resource = Resource(status="ACTIVE")
    assert resource.status == ResourceStatus.ACTIVE
    
    # Invalid value
    with pytest.raises(ValidationError):
        Resource(status="INVALID")
```

## Migration Guide

### From Magic Strings to Enums

```python
# Before - Magic strings (typo-prone, no type safety)
def process_resource(status: str):
    if status == "ACTIVE":
        ...

# After - Enums (type-safe, IDE support)
class ResourceStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

def process_resource(status: ResourceStatus):
    if status == ResourceStatus.ACTIVE:
        ...
```

### From Constants to Enums

```python
# Before - Module constants (mutable, no validation)
STATUS_ACTIVE = "ACTIVE"
STATUS_INACTIVE = "INACTIVE"

# After - Enum (immutable, validated)
class ResourceStatus(StrEnum):
    """Resource status states."""
    
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
```

## References

- **Python Docs**: [enum — Support for enumerations](https://docs.python.org/3/library/enum.html)
- **PEP 435**: Adding an Enum type to Python
- **Pydantic**: [Field Types - Enums](https://docs.pydantic.dev/latest/usage/types/enums/)
- **FastAPI**: [Query Parameters - Enum](https://fastapi.tiangolo.com/tutorial/query-params/#predefined-values)
- **DDD**: Domain-Driven Design - Value Objects and Type Safety

---

**Related Documentation:**
- `Value_Objects.md` - For complex domain values
- `Entities.md` - For objects with identity
- `Exceptions.md` - For error handling patterns

