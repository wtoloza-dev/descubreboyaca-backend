# Domain Value Objects

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Value Objects** | `Domain Layer` | `DDD` `Value Objects` `Immutability` |

## Definition

Value Objects are immutable objects defined by their values rather than an identity. In DDD, two value objects with the same values are considered identical and interchangeable. They encapsulate domain concepts that are described by their attributes.

**Key Characteristics:**
- **No Identity**: Defined by attributes, not by an ID
- **Immutable**: Cannot be modified after creation
- **Equality by Value**: Two instances with same values are equal
- **Self-Validating**: Enforce invariants in constructor
- **Side-Effect Free**: Operations return new instances

## Types of Value Objects

### 1. Pure Value Objects
Standalone immutable domain concepts (e.g., `SemanticVersion`, `Pagination`).

### 2. Entity Data Value Objects
Value objects that represent entity data without identity (e.g., `PromptData`, `PromptVersionData`).  
**Note**: These are covered in detail in `Entities.md`.

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Directory | `value_objects/` | `app/domains/prompt/domain/value_objects/` |
| Filename | `{concept}_snake_case.py` | `semantic_version.py` |
| Class Name | `{Concept}PascalCase` | `SemanticVersion` |

## Implementation Rules

### Basic Structure

```python
"""[Concept] value object."""

from pydantic import BaseModel, ConfigDict, Field


class XxxValue(BaseModel):
    """[Concept] value object description.
    
    [Brief explanation of what it represents and why it's immutable].
    
    Attributes:
        field1: Description.
        field2: Description.
    """
    
    model_config = ConfigDict(frozen=True)
    
    field1: str = Field(description="Description")
    field2: int = Field(ge=0, description="Description with validation")
```

### Class Structure Order

1. **Module docstring**
2. **Imports** (standard lib, third-party, local)
3. **Class docstring**
4. **`model_config`** (with `frozen=True` for immutability)
5. **Field definitions** (with validation constraints)
6. **Validators** (if needed)
7. **Factory methods** (`@classmethod` constructors)
8. **Business methods** (returning new instances)
9. **Conversion methods** (`to_string()`, `to_dict()`, etc.)
10. **Dunder methods** (`__str__`, `__repr__`, `__eq__`, etc.)

### Immutability

**Always use `frozen=True`** in `model_config` to ensure immutability:

```python
model_config = ConfigDict(frozen=True)
```

This prevents modification after creation:
```python
version = SemanticVersion(major=1, minor=0, patch=0)
version.major = 2  # ❌ Raises ValidationError
```

### Type Annotations

- **Use primitive types**: `str`, `int`, `float`, `bool`, `dict`, `list`
- **No custom types**: Avoid `ULID`, `UUID`, or other non-primitive types
- **Use constraints**: `ge`, `gt`, `le`, `lt`, `min_length`, `max_length`

**Examples:**
```python
# ✅ CORRECT - Primitives with validation
major: int = Field(ge=0, description="Major version number")
name: str = Field(min_length=1, max_length=100, description="Name")
ratio: float = Field(ge=0.0, le=1.0, description="Ratio between 0 and 1")

# ❌ INCORRECT - Custom types
from ulid import ULID
id: ULID = Field(description="Identifier")
```

### Factory Methods

Use `@classmethod` for alternative constructors:

```python
@classmethod
def from_string(cls, version: str) -> "SemanticVersion":
    """Parse a semantic version string.
    
    Args:
        version: Version string in format "major.minor.patch".
        
    Returns:
        SemanticVersion: Parsed semantic version object.
        
    Raises:
        InvalidVersionFormatException: If version format is invalid.
    """
    parts = version.split(".")
    major, minor, patch = [int(part) for part in parts]
    return cls(major=major, minor=minor, patch=patch)
```

### Business Methods

Methods should return **new instances** (never mutate):

```python
def increment_major(self) -> "SemanticVersion":
    """Create new version with incremented major.
    
    Returns:
        SemanticVersion: New version with major incremented.
    """
    return SemanticVersion(major=self.major + 1, minor=0, patch=0)
```

### Validation

Use Pydantic validators for complex validation:

```python
@field_validator("email")
@classmethod
def validate_email(cls, v: str) -> str:
    """Validate email format.
    
    Args:
        v: Email string to validate.
        
    Returns:
        str: Validated email.
        
    Raises:
        ValueError: If email format is invalid.
    """
    if "@" not in v:
        raise ValueError("Invalid email format")
    return v.lower()
```

## Documentation Template

### Simple Value Object

```python
"""[Concept] value object."""

from pydantic import BaseModel, ConfigDict, Field


class XxxValue(BaseModel):
    """[Concept] value object description.
    
    Immutable value object representing [what it represents].
    
    Attributes:
        field1: Description.
        field2: Description.
    """
    
    model_config = ConfigDict(frozen=True)
    
    field1: str = Field(description="Description")
    field2: int = Field(ge=0, description="Description")
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.field1}:{self.field2}"
```

### Value Object with Factory Methods

```python
"""[Concept] value object."""

from pydantic import BaseModel, ConfigDict, Field


class XxxValue(BaseModel):
    """[Concept] value object description.
    
    Immutable value object representing [what it represents].
    
    Attributes:
        field1: Description.
        field2: Description.
    """
    
    model_config = ConfigDict(frozen=True)
    
    field1: str = Field(description="Description")
    field2: int = Field(ge=0, description="Description")
    
    @classmethod
    def from_string(cls, value: str) -> "XxxValue":
        """Parse from string format.
        
        Args:
            value: String to parse.
            
        Returns:
            XxxValue: Parsed value object.
            
        Raises:
            ValueError: If format is invalid.
        """
        field1, field2 = value.split(":")
        return cls(field1=field1, field2=int(field2))
    
    def to_string(self) -> str:
        """Convert to string format.
        
        Returns:
            str: String representation.
        """
        return f"{self.field1}:{self.field2}"
    
    def with_field1(self, new_field1: str) -> "XxxValue":
        """Create new instance with different field1.
        
        Args:
            new_field1: New value for field1.
            
        Returns:
            XxxValue: New instance with updated field1.
        """
        return XxxValue(field1=new_field1, field2=self.field2)
    
    def __str__(self) -> str:
        """String representation."""
        return self.to_string()
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"XxxValue({self.field1}:{self.field2})"
```

## Real-World Examples

### Example 1: SemanticVersion

```python
# Creating instances
v1 = SemanticVersion(major=1, minor=0, patch=0)
v2 = SemanticVersion.from_string("1.2.3")

# Immutability
v1.major = 2  # ❌ Raises ValidationError

# New instances from operations
v3 = v1.increment_major()  # Returns SemanticVersion(2, 0, 0)
v4 = v2.increment_minor()  # Returns SemanticVersion(1, 3, 0)

# Value equality
assert SemanticVersion(1, 0, 0) == SemanticVersion(1, 0, 0)  # ✅ True
```

### Example 2: Pagination

```python
# Creating instances
page1 = Pagination(page=1, size=20)

# Computed fields
assert page1.offset == 0   # (1-1) * 20
assert page1.limit == 20   # size

# Immutability
page1.page = 2  # ❌ Raises ValidationError

# Create new instance for next page
page2 = Pagination(page=2, size=20)
assert page2.offset == 20  # (2-1) * 20
```

## Common Patterns

### Pattern 1: Self-Validation

```python
class Email(BaseModel):
    """Email value object."""
    
    model_config = ConfigDict(frozen=True)
    
    value: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    
    @classmethod
    def create(cls, email: str) -> "Email":
        """Create validated email."""
        return cls(value=email.lower().strip())
```

### Pattern 2: Rich Behavior

```python
class Money(BaseModel):
    """Money value object."""
    
    model_config = ConfigDict(frozen=True)
    
    amount: float = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    
    def add(self, other: "Money") -> "Money":
        """Add two money values (same currency)."""
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)
    
    def multiply(self, factor: float) -> "Money":
        """Multiply money by a factor."""
        return Money(amount=self.amount * factor, currency=self.currency)
```

### Pattern 3: Complex Parsing

```python
class DateRange(BaseModel):
    """Date range value object."""
    
    model_config = ConfigDict(frozen=True)
    
    start: str = Field(description="Start date ISO format")
    end: str = Field(description="End date ISO format")
    
    @classmethod
    def from_string(cls, range_str: str) -> "DateRange":
        """Parse from 'YYYY-MM-DD to YYYY-MM-DD' format."""
        start, end = range_str.split(" to ")
        return cls(start=start.strip(), end=end.strip())
    
    @field_validator("end")
    @classmethod
    def validate_end_after_start(cls, v: str, info) -> str:
        """Ensure end is after start."""
        if "start" in info.data and v < info.data["start"]:
            raise ValueError("End date must be after start date")
        return v
```

## Required Elements Checklist

- [ ] Module docstring describing the concept
- [ ] Class inherits from `BaseModel`
- [ ] `model_config = ConfigDict(frozen=True)` for immutability
- [ ] All fields use primitive types with validation
- [ ] Comprehensive docstrings (class, methods, attributes)
- [ ] Factory methods use `@classmethod`
- [ ] Business methods return new instances (no mutation)
- [ ] Proper `__str__` and `__repr__` implementations
- [ ] Exported in `__init__.py`
- [ ] No identity field (no `id`)

## Anti-Patterns to Avoid

### ❌ Mutable Value Objects

```python
# BAD - Missing frozen=True
class Version(BaseModel):
    major: int
    minor: int
    
v = Version(major=1, minor=0)
v.major = 2  # ❌ Should not be allowed
```

### ❌ Value Objects with Identity

```python
# BAD - Value objects should not have IDs
class Color(BaseModel):
    id: str  # ❌ No identity in value objects
    red: int
    green: int
    blue: int
```

### ❌ Mutation Methods

```python
# BAD - Methods that mutate state
class Counter(BaseModel):
    model_config = ConfigDict(frozen=True)
    count: int
    
    def increment(self) -> None:  # ❌ Should return new instance
        self.count += 1  # Will raise error due to frozen=True
```

### ❌ Missing Validation

```python
# BAD - No validation on fields
class Age(BaseModel):
    value: int  # ❌ Should validate: ge=0, le=150
```

## Best Practices

1. **Keep them small**: Focus on a single cohesive concept
2. **Make them expressive**: Use meaningful names and methods
3. **Validate in constructor**: Ensure invariants are always met
4. **Provide factory methods**: Make construction convenient
5. **Return new instances**: Never mutate, always create new
6. **Override `__str__` and `__repr__`**: Improve debugging
7. **Use type hints**: Make the code self-documenting
8. **Write comprehensive docs**: Explain what, why, and how

## When to Use Value Objects

✅ **Use Value Objects for:**
- Domain concepts without identity (dates, money, colors, coordinates)
- Immutable data structures (configuration, constants)
- Validated primitives (email, phone, URL)
- Complex calculations (ranges, formulas)
- Multi-field concepts treated as single unit

❌ **Don't Use Value Objects for:**
- Things with identity (users, orders, products) → Use Entities
- Mutable state → Use regular classes
- Simple primitives without validation → Use built-in types
- Infrastructure concerns → Use different patterns

## References

- **Entities.md**: For `*Data` value objects used in entities
- **DDD Blue Book**: Evans, Eric. "Domain-Driven Design"
- **Implementing DDD**: Vernon, Vaughn. Chapter on Value Objects

