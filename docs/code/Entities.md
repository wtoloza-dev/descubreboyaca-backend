# Domain Entities

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Domain Entities** | `Domain Layer` | `DDD` `Entities` `Business Logic` |

## Definition

Entities are objects with unique identity and lifecycle. In DDD, they represent core domain concepts that are distinguished by their ID, not just their attributes.

## Pattern

**Entity = Value Object + Identity + Audit**

```
PromptData (Value Object) + Audit (Identity & Lifecycle) = Prompt (Entity)
```

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Filename | `{entity}_snake_case.py` | `prompt_version.py` |
| Value Object Class | `{Entity}Data` | `PromptVersionData` |
| Entity Class | `{Entity}` | `PromptVersion` |

## Implementation Rules

### Entity Structure
```python
class Xxx(XxxData, Audit):
    """Entity with identity and audit trail.
    
    [One sentence explaining what it represents].
    """
    # No model_config needed here (inherited from XxxData and Audit)
```

**Key Points:**
- Always inherit from both `XxxData` and `Audit` (in that order)
- Multiple inheritance: Data first, then Audit
- Can have `pass` body if no additional logic
- **No `model_config` in Entity classes** (inherited from parent classes)

### Class Structure Order (Standard)
```python
class XxxData(BaseModel):
    """Docstring."""
    
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)  # ← Always first
    
    # Then field definitions
    field1: str = Field(...)
    field2: int = Field(...)
    
    # Then validators (if any)
    @field_validator("field1")
    @classmethod
    def validate_field1(cls, v):
        ...
```

**Standard Order:**
1. Class docstring
2. `model_config` (immediately after docstring)
3. Field definitions
4. Validators and methods

### Type Annotations
- **Use primitive types** for all fields, especially IDs
- **IDs must be `str`**, never `ULID` or other custom types
- Avoid importing `ulid.ULID` in entity files
- The infrastructure layer handles ULID generation/conversion

**Examples:**
```python
# ✅ CORRECT - Use primitive str
prompt_id: str = Field(description="Prompt identifier")
user_id: str | None = Field(None, description="User identifier")

# ❌ INCORRECT - Don't use ULID type
from ulid import ULID
prompt_id: str | ULID | None = Field(None, description="Prompt ID")
```

### Required Elements
- ✅ Module docstring with "domain entities following DDD principles"
- ✅ Class docstring explaining purpose
- ✅ Import `Audit` from `app.shared.domain.entities`
- ✅ `model_config` at the top (Value Objects only, not Entities)
- ✅ Use primitive types (`str`, `int`, `bool`, etc.) for all fields

## Documentation Template

```python
"""[Entity name] domain entities following DDD principles."""

from app.shared.domain.entities import Audit


class XxxData(BaseModel):
    """[Entity] business data (Value Object).
    
    Attributes:
        field1: Description.
        field2: Description.
    """
    
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)
    
    field1: str = Field(description="Description")
    field2: int = Field(description="Description")


class Xxx(XxxData, Audit):
    """[Entity] entity with identity and audit fields.
    
    [One sentence explaining what it represents].
    """
```

## Checklist

- [ ] Inherits from `XxxData` and `Audit` (in that order)
- [ ] Has proper docstring
- [ ] `model_config` at the top (Value Object only)
- [ ] No business logic (entities are data containers)
- [ ] Uses primitive types (especially `str` for IDs, never `ULID`)
- [ ] No imports of `ulid.ULID` in entity files
- [ ] Exported in `__init__.py`

