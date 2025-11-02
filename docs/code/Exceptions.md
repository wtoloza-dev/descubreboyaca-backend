# Domain Exceptions

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Domain Exceptions** | `Domain Layer` | `DDD` `Error Handling` `Clean Architecture` |

## Definition

Domain Exceptions represent errors that occur during the execution of business logic. They are domain-specific errors that express business rules violations or invalid states. These exceptions maintain clean architecture boundaries by keeping domain concerns separate from infrastructure concerns.

**Key Characteristics:**
- **Domain-Specific**: Express business rule violations
- **Self-Describing**: Include error_code, message, and context
- **HTTP-Agnostic**: No coupling to HTTP status codes (mapping happens in infrastructure layer)
- **Contextual**: Carry structured information about the error
- **Typed**: Each exception type represents a specific error condition

## Exception Hierarchy

```
DomainException (Base)
│
├── NotFoundException (404)
│   ├── PromptNotFoundException
│   ├── PromptVersionNotFoundException
│   ├── PromptHistoryNotFoundException
│   └── OwnershipNotFoundException
│
├── AlreadyExistsException (409)
│   ├── PromptAlreadyExistsException
│   └── OwnershipAlreadyExistsException
│
├── ValidationException (422)
│   ├── InvalidVersionFormatException
│   ├── InvalidVersionPartsException
│   ├── InvalidVersionStructureException
│   ├── InvalidVersionTypeException
│   └── VersionConflictException
│
├── ForbiddenException (403)
│   └── InsufficientAccessException
│
└── UnauthorizedException (401)
```

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Directory | `domain/exceptions/` | `app/domains/prompt/domain/exceptions/` |
| Filename | `{concept}_snake_case.py` | `prompt_version.py`, `ownership.py` |
| Class Name | `{Concept}{ExceptionType}` | `PromptNotFoundException` |
| Error Code | `UPPER_SNAKE_CASE` | `PROMPT_NOT_FOUND` |

## Implementation Rules

### Basic Structure

```python
"""[Concept] domain exceptions."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class EntityNotFoundException(NotFoundException):
    """Exception raised when entity is not found.
    
    Example:
        >>> raise EntityNotFoundException(
        ...     entity_id="01HQ123ABC",
        ...     context={"operation": "update"}
        ... )
    """
    
    def __init__(
        self,
        entity_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize entity not found exception.
        
        Args:
            entity_id: ID of the entity that was not found.
            context: Additional context about the operation.
        """
        full_context = {"entity_id": entity_id, **(context or {})}
        super().__init__(
            message=f"Entity with ID '{entity_id}' not found",
            context=full_context,
            error_code="ENTITY_NOT_FOUND",
        )
```

### Class Structure Order

1. **Module docstring**
2. **Imports** (standard lib, third-party, local, base exceptions)
3. **Class docstring** (with example)
4. **`__init__` method** with proper signature
5. **Context building** (merge provided context with exception-specific context)
6. **`super().__init__()` call** with message, context, and error_code

### Exception Naming Convention

Follow this pattern: `{Domain}{Condition}Exception`

**Examples:**
- `PromptNotFoundException` - Prompt not found
- `PromptAlreadyExistsException` - Prompt already exists
- `InvalidVersionFormatException` - Version format is invalid
- `InsufficientAccessException` - Insufficient access level

### Error Code Convention

- **Format**: `UPPER_SNAKE_CASE`
- **Pattern**: Should match exception name semantically
- **Consistency**: Same error code for same error across domains

**Examples:**
```python
PromptNotFoundException → "PROMPT_NOT_FOUND"
PromptAlreadyExistsException → "PROMPT_ALREADY_EXISTS"
InvalidVersionFormatException → "INVALID_VERSION_FORMAT"
InsufficientAccessException → "INSUFFICIENT_ACCESS"
```

### Base Exception Types

#### 1. NotFoundException (404)

Used when a requested resource doesn't exist.

```python
class PromptNotFoundException(NotFoundException):
    """Exception raised when a prompt is not found."""
    
    def __init__(
        self,
        prompt_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        full_context = {"prompt_id": prompt_id, **(context or {})}
        super().__init__(
            message=f"Prompt with ID '{prompt_id}' not found",
            context=full_context,
            error_code="PROMPT_NOT_FOUND",
        )
```

#### 2. AlreadyExistsException (409)

Used when attempting to create a duplicate resource.

```python
class PromptAlreadyExistsException(AlreadyExistsException):
    """Exception raised when attempting to create a duplicate prompt."""
    
    def __init__(
        self,
        prompt_name: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        full_context = {"prompt_name": prompt_name, **(context or {})}
        super().__init__(
            message=f"Prompt with name '{prompt_name}' already exists",
            context=full_context,
            error_code="PROMPT_ALREADY_EXISTS",
        )
```

#### 3. ValidationException (422)

Used when input data doesn't meet validation rules.

```python
class InvalidVersionFormatException(ValidationException):
    """Exception raised when version format is invalid."""
    
    def __init__(
        self,
        version: str,
        reason: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        message = f"Invalid version format '{version}'"
        if reason:
            message += f": {reason}"
        
        full_context = {
            "version": version,
            **({"reason": reason} if reason else {}),
            **(context or {}),
        }
        super().__init__(
            message=message,
            context=full_context,
            error_code="INVALID_VERSION_FORMAT",
        )
```

#### 4. ForbiddenException (403)

Used when user lacks permission to perform an action.

```python
class InsufficientAccessException(ForbiddenException):
    """Exception raised when user lacks required access level."""
    
    def __init__(
        self,
        prompt_id: str,
        owner_id: str,
        required_level: AccessLevel,
        current_level: AccessLevel | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        message = (
            f"Insufficient access to prompt '{prompt_id}'. "
            f"Required: {required_level.value}"
        )
        if current_level:
            message += f", Current: {current_level.value}"
        
        full_context = {
            "prompt_id": prompt_id,
            "owner_id": owner_id,
            "required_level": required_level.value,
            **({"current_level": current_level.value} if current_level else {}),
            **(context or {}),
        }
        
        super().__init__(
            message=message,
            context=full_context,
            error_code="INSUFFICIENT_ACCESS",
        )
```

#### 5. UnauthorizedException (401)

Used when authentication is required or has failed.

```python
class InvalidCredentialsException(UnauthorizedException):
    """Exception raised when authentication credentials are invalid."""
    
    def __init__(
        self,
        username: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        full_context = {"username": username, **(context or {})}
        super().__init__(
            message=f"Invalid credentials for user '{username}'",
            context=full_context,
            error_code="INVALID_CREDENTIALS",
        )
```

### Context Building Pattern

Always merge provided context with exception-specific context:

```python
def __init__(
    self,
    entity_id: str,
    field: str,
    context: dict[str, Any] | None = None,
) -> None:
    # Merge exception-specific data with provided context
    full_context = {
        "entity_id": entity_id,
        "field": field,
        **(context or {}),  # User-provided context has priority
    }
    super().__init__(
        message=f"Validation failed for field '{field}' in entity '{entity_id}'",
        context=full_context,
        error_code="VALIDATION_FAILED",
    )
```

### Optional Parameters

Use conditional dictionary merging for optional parameters:

```python
full_context = {
    "required_field": value,
    **({"optional_field": optional_value} if optional_value else {}),
    **(context or {}),
}
```

## Registration in Infrastructure Layer

**⚠️ CRITICAL**: All domain exceptions **MUST** be registered in `app/core/errors/mappers.py` to be properly handled by the application.

### Step 1: Import the Exception

```python
# app/core/errors/mappers.py
from app.domains.prompt.domain.exceptions import (
    PromptNotFoundException,
    PromptAlreadyExistsException,
    # ... add your new exception here
)
```

### Step 2: Map to HTTP Status Code

```python
class DomainExceptionMapper:
    """Maps domain exceptions to HTTP status codes and error details."""
    
    EXCEPTION_STATUS_MAP: dict[type[DomainException], int] = {
        # Not Found errors -> 404
        PromptNotFoundException: status.HTTP_404_NOT_FOUND,
        
        # Already Exists errors -> 409 Conflict
        PromptAlreadyExistsException: status.HTTP_409_CONFLICT,
        
        # Forbidden errors -> 403
        InsufficientAccessException: status.HTTP_403_FORBIDDEN,
        
        # Validation errors -> 422 Unprocessable Content
        InvalidVersionFormatException: status.HTTP_422_UNPROCESSABLE_CONTENT,
        
        # Unauthorized errors -> 401
        InvalidCredentialsException: status.HTTP_401_UNAUTHORIZED,
        
        # Add your new exception mapping here
    }
```

### HTTP Status Code Guidelines

| Exception Type | HTTP Status | When to Use |
|---------------|-------------|-------------|
| `NotFoundException` | 404 | Resource doesn't exist |
| `AlreadyExistsException` | 409 | Duplicate resource |
| `ValidationException` | 422 | Invalid input data |
| `ForbiddenException` | 403 | Insufficient permissions |
| `UnauthorizedException` | 401 | Authentication required/failed |
| `DomainException` (custom) | 400 | Generic business rule violation |
| `DomainException` (unhandled) | 500 | Unexpected domain error |

## Documentation Template

### Single Parameter Exception

```python
"""[Entity] domain exceptions."""

from typing import Any

from app.shared.domain.exceptions import NotFoundException


class EntityNotFoundException(NotFoundException):
    """Exception raised when an entity is not found.
    
    Example:
        >>> raise EntityNotFoundException(entity_id="01HQ123ABC")
    """
    
    def __init__(
        self,
        entity_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize entity not found exception.
        
        Args:
            entity_id: ID of the entity not found.
            context: Additional context.
        """
        full_context = {"entity_id": entity_id, **(context or {})}
        super().__init__(
            message=f"Entity with ID '{entity_id}' not found",
            context=full_context,
            error_code="ENTITY_NOT_FOUND",
        )
```

### Multi-Parameter Exception

```python
"""Ownership domain exceptions."""

from typing import Any

from app.shared.domain.exceptions import AlreadyExistsException

from ..enums import OwnerType


class OwnershipAlreadyExistsException(AlreadyExistsException):
    """Exception raised when ownership already exists for owner.
    
    Example:
        >>> raise OwnershipAlreadyExistsException(
        ...     prompt_id="01HQ123ABC",
        ...     owner_type=OwnerType.USER,
        ...     owner_id="user123",
        ... )
    """
    
    def __init__(
        self,
        prompt_id: str,
        owner_type: OwnerType,
        owner_id: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ownership already exists exception.
        
        Args:
            prompt_id: ID of the prompt.
            owner_type: Type of owner.
            owner_id: ID of the owner.
            context: Additional context.
        """
        full_context = {
            "prompt_id": prompt_id,
            "owner_type": owner_type.value,
            "owner_id": owner_id,
            **(context or {}),
        }
        super().__init__(
            message=f"Ownership for {owner_type.value} '{owner_id}' already exists on prompt '{prompt_id}'",
            context=full_context,
            error_code="OWNERSHIP_ALREADY_EXISTS",
        )
```

### Exception with Optional Parameters

```python
"""Version validation domain exceptions."""

from typing import Any

from app.shared.domain.exceptions import ValidationException


class InvalidVersionFormatException(ValidationException):
    """Exception raised when version format is invalid.
    
    Example:
        >>> raise InvalidVersionFormatException(version="1.2", reason="Missing patch")
    """
    
    def __init__(
        self,
        version: str,
        reason: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize invalid version format exception.
        
        Args:
            version: Invalid version string.
            reason: Specific reason for invalidity.
            context: Additional context.
        """
        message = f"Invalid version format '{version}'"
        if reason:
            message += f": {reason}"
        
        full_context = {
            "version": version,
            **({"reason": reason} if reason else {}),
            **(context or {}),
        }
        super().__init__(
            message=message,
            context=full_context,
            error_code="INVALID_VERSION_FORMAT",
        )
```

## Package Structure

### Exception Module (`exceptions/__init__.py`)

```python
"""[Domain] domain exceptions package."""

from .entity import EntityNotFoundException, EntityAlreadyExistsException
from .validation import InvalidDataException


__all__ = [
    # Entity exceptions
    "EntityNotFoundException",
    "EntityAlreadyExistsException",
    # Validation exceptions
    "InvalidDataException",
]
```

## Best Practices

### ✅ DO

1. **Inherit from appropriate base exception**
   ```python
   class PromptNotFoundException(NotFoundException):  # ✅
   ```

2. **Provide meaningful error messages**
   ```python
   message=f"Prompt with ID '{prompt_id}' not found"  # ✅
   ```

3. **Include relevant context**
   ```python
   full_context = {"prompt_id": prompt_id, "operation": "delete"}  # ✅
   ```

4. **Use type hints**
   ```python
   def __init__(self, prompt_id: str, context: dict[str, Any] | None = None) -> None:  # ✅
   ```

5. **Provide usage examples in docstring**
   ```python
   """
   Example:
       >>> raise PromptNotFoundException(prompt_id="01HQ123ABC")
   """
   ```

6. **Make context optional with default None**
   ```python
   context: dict[str, Any] | None = None  # ✅
   ```

7. **Use consistent error code format**
   ```python
   error_code="PROMPT_NOT_FOUND"  # ✅ UPPER_SNAKE_CASE
   ```

8. **Register in mapper immediately**
   ```python
   # In app/core/errors/mappers.py
   PromptNotFoundException: status.HTTP_404_NOT_FOUND,  # ✅
   ```

### ❌ DON'T

1. **Don't create generic Exception**
   ```python
   class Error(Exception):  # ❌ Too generic
   ```

2. **Don't hardcode HTTP status codes in domain**
   ```python
   self.status_code = 404  # ❌ Infrastructure concern
   ```

3. **Don't forget context parameter**
   ```python
   def __init__(self, prompt_id: str) -> None:  # ❌ Missing context param
   ```

4. **Don't mutate input context**
   ```python
   context["prompt_id"] = prompt_id  # ❌ Mutating input
   full_context = {"prompt_id": prompt_id, **(context or {})}  # ✅ Creating new
   ```

5. **Don't use inconsistent error codes**
   ```python
   error_code="prompt-not-found"  # ❌ Use UPPER_SNAKE_CASE
   error_code="PromptNotFound"    # ❌ Not UPPER_SNAKE_CASE
   ```

6. **Don't forget to export in `__init__.py`**
   ```python
   # Missing from __all__  # ❌
   ```

7. **Don't skip docstrings or examples**
   ```python
   class MyException(NotFoundException):  # ❌ No docstring
       def __init__(self, ...):  # ❌ No example
   ```

## Required Elements Checklist

- [ ] Module docstring describing exception purpose
- [ ] Import appropriate base exception from `app.shared.domain.exceptions`
- [ ] Class inherits from correct base exception type
- [ ] Class docstring with description
- [ ] Usage example in docstring
- [ ] `__init__` method with proper type hints
- [ ] `__init__` docstring (Google style)
- [ ] Context parameter with default `None`
- [ ] Context merging: `full_context = {specific_data, **(context or {})}`
- [ ] Meaningful error message
- [ ] Consistent error_code in UPPER_SNAKE_CASE
- [ ] Exported in `__init__.py`
- [ ] **Registered in `app/core/errors/mappers.py`**

## Common Patterns

### Pattern 1: Simple Not Found

```python
class XxxNotFoundException(NotFoundException):
    """Exception raised when xxx is not found."""
    
    def __init__(self, xxx_id: str, context: dict[str, Any] | None = None) -> None:
        full_context = {"xxx_id": xxx_id, **(context or {})}
        super().__init__(
            message=f"Xxx with ID '{xxx_id}' not found",
            context=full_context,
            error_code="XXX_NOT_FOUND",
        )
```

### Pattern 2: Conflict with Multiple Fields

```python
class XxxConflictException(AlreadyExistsException):
    """Exception raised when xxx conflicts with existing data."""
    
    def __init__(
        self,
        field1: str,
        field2: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        full_context = {"field1": field1, "field2": field2, **(context or {})}
        super().__init__(
            message=f"Xxx with {field1}={field1} and {field2}={field2} already exists",
            context=full_context,
            error_code="XXX_CONFLICT",
        )
```

### Pattern 3: Validation with Reason

```python
class InvalidXxxException(ValidationException):
    """Exception raised when xxx validation fails."""
    
    def __init__(
        self,
        value: str,
        reason: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        message = f"Invalid xxx value '{value}'"
        if reason:
            message += f": {reason}"
        
        full_context = {
            "value": value,
            **({"reason": reason} if reason else {}),
            **(context or {}),
        }
        super().__init__(
            message=message,
            context=full_context,
            error_code="INVALID_XXX",
        )
```

### Pattern 4: Permission Denied

```python
class InsufficientXxxPermissionException(ForbiddenException):
    """Exception raised when user lacks required xxx permission."""
    
    def __init__(
        self,
        user_id: str,
        resource_id: str,
        required_permission: str,
        context: dict[str, Any] | None = None,
    ) -> None:
        full_context = {
            "user_id": user_id,
            "resource_id": resource_id,
            "required_permission": required_permission,
            **(context or {}),
        }
        super().__init__(
            message=f"User '{user_id}' lacks '{required_permission}' permission for resource '{resource_id}'",
            context=full_context,
            error_code="INSUFFICIENT_XXX_PERMISSION",
        )
```

## When to Create New Exceptions

✅ **Create New Exception When:**
- Represents a specific business rule violation
- Requires different handling or HTTP status code
- Carries domain-specific context
- Helps with debugging and monitoring
- Makes error handling more explicit

❌ **Don't Create New Exception When:**
- Generic base exception is sufficient
- Only message differs (use context instead)
- No business logic distinction
- Over-fragmenting error hierarchy

## Testing Exceptions

```python
import pytest
from app.domains.prompt.domain.exceptions import PromptNotFoundException


def test_prompt_not_found_exception():
    """Test PromptNotFoundException structure."""
    prompt_id = "01HQ123ABC"
    context = {"operation": "update"}
    
    exc = PromptNotFoundException(prompt_id=prompt_id, context=context)
    
    assert exc.error_code == "PROMPT_NOT_FOUND"
    assert prompt_id in exc.message
    assert exc.context["prompt_id"] == prompt_id
    assert exc.context["operation"] == "update"


def test_exception_is_raised():
    """Test that exception can be raised and caught."""
    with pytest.raises(PromptNotFoundException) as exc_info:
        raise PromptNotFoundException(prompt_id="test123")
    
    assert exc_info.value.error_code == "PROMPT_NOT_FOUND"
```

## References

- **Entities.md**: For domain entities
- **Value_Objects.md**: For value objects
- **Clean Architecture**: Infrastructure layer handles HTTP concerns
- **DDD**: Domain exceptions express business rules

