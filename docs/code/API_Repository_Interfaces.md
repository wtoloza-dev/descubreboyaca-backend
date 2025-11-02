# API Repository Interfaces

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **API Repository Interfaces** | `Domain Layer` | `Hexagonal Architecture` `Ports` `Protocol` |

## Definition

API Repository Interfaces are Protocol-based contracts in the domain layer that define how the domain interacts with external services. They enable dependency inversion - the domain depends on abstractions, and infrastructure provides implementations.

## Pattern

**Interface (Port) = Protocol + Async Methods + Domain Types**

```
External Service → REST Implementation (Adapter) → Interface (Port) ← Domain Logic
```

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Directory | `domain/interfaces/` | `domain/interfaces/` |
| Filename | `{service}_api_repository.py` | `genai_api_repository.py` |
| Interface Class | `{Service}APIRepositoryInterface` | `GenAIAPIRepositoryInterface` |
| Implementation | `REST{Service}APIRepository` | `RESTGenAIAPIRepository` |

## Implementation Rules

### Protocol Structure

```python
class XxxAPIRepositoryInterface(Protocol):
    """Docstring with purpose.
    
    Implementations:
        - RESTXxxAPIRepository: REST/HTTP implementation
    """
    
    async def method_name(self, param: Type) -> ReturnType:
        """Method docstring.
        
        Args:
            param: Description.
            
        Returns:
            Description.
            
        Raises:
            ExceptionType: Description.
        """
        ...
```

**Key Points:**
- Always use `Protocol` from `typing` (NOT `ABC`)
- All methods must be `async`
- All methods end with `...` (NOT `pass`)
- Return domain value objects (NOT raw dicts)
- Complete docstrings with Args, Returns, Raises

### Method Organization

**Standard Order:**
1. List/Query methods (get_items, list_resources)
2. Action methods (perform_action, execute_task)
3. Single item methods (get_item, get_resource)

### Type Annotations

- **Use domain value objects** for all parameters and returns
- **Never return `dict` or `Any`**
- **Use `| None` for optional returns**
- Use primitive types for IDs (`str`, not custom types)

**Examples:**
```python
# ✅ CORRECT - Domain value objects
async def get_items(self) -> list[ServiceItem]: ...
async def get_item(self, item_id: str) -> ServiceItem | None: ...
async def perform_action(self, request: ServiceRequest) -> ServiceResponse: ...

# ❌ INCORRECT - Raw dicts or Any
async def get_items(self) -> list[dict]: ...
async def get_item(self, item_id: str) -> Any: ...
```

### Required Elements

- ✅ Module docstring explaining purpose and pattern
- ✅ Use `Protocol` from `typing`
- ✅ All methods are `async`
- ✅ Methods end with `...` (not `pass`)
- ✅ Complete docstrings (Args, Returns, Raises)
- ✅ Type hints for all parameters and returns
- ✅ Document implementations in class docstring

### Prohibited Elements

- ❌ Don't use `ABC` or `abstractmethod`
- ❌ Don't return `dict`, `Any`, or raw data
- ❌ Don't include business logic
- ❌ Don't add transaction methods (commit, rollback)
- ❌ Don't add audit parameters (created_by, updated_by)
- ❌ Don't create HTTP client in interface

## Documentation Template

```python
"""[Service] API repository interface (Port).

This module defines the repository protocol (port) for [Service] API operations,
following the hexagonal architecture pattern.
"""

from typing import Protocol

from ..value_objects import ServiceRequest, ServiceResponse


class ServiceAPIRepositoryInterface(Protocol):
    """[Service] API repository protocol interface (Port).
    
    Implementations:
        - RESTServiceAPIRepository: REST/HTTP implementation
    """
    
    async def get_items(self) -> list[ServiceItem]:
        """Get items from external service.
        
        Returns:
            List of service items.
            
        Raises:
            ServiceException: If the request fails.
            ValidationException: If response format is invalid.
        """
        ...
    
    async def perform_action(self, request: ServiceRequest) -> ServiceResponse:
        """Perform action via external service.
        
        Args:
            request: Request data for the action.
            
        Returns:
            Service response.
            
        Raises:
            ServiceException: If the request fails.
        """
        ...
    
    async def get_item(self, item_id: str) -> ServiceItem | None:
        """Get specific item by ID.
        
        Args:
            item_id: Item identifier.
            
        Returns:
            Item if found, None otherwise.
            
        Raises:
            ServiceException: If the request fails.
        """
        ...
```

## Common Patterns

### Pattern 1: Read-Only API
```python
async def get_items(self) -> list[Item]: ...
async def get_item(self, item_id: str) -> Item | None: ...
async def search_items(self, query: str) -> list[Item]: ...
```

### Pattern 2: Action-Based API
```python
async def process_data(self, data: Request) -> Result: ...
async def get_job_status(self, job_id: str) -> JobStatus: ...
async def cancel_job(self, job_id: str) -> bool: ...
```

### Pattern 3: Full CRUD API
```python
async def list_resources(self) -> list[Resource]: ...
async def get_resource(self, id: str) -> Resource | None: ...
async def create_resource(self, data: Data) -> Resource: ...
async def update_resource(self, id: str, data: Data) -> Resource | None: ...
async def delete_resource(self, id: str) -> bool: ...
```

## Return Type Guidelines

| Operation | Return Type | Example |
|-----------|-------------|---------|
| List items | `list[Model]` | `list[GenaiModel]` |
| Single item | `Model \| None` | `GenaiModel \| None` |
| Action | `Response` | `GenaiResponse` |
| Boolean check | `bool` | `bool` |
| Count | `int` | `int` |

## Error Handling

**Interfaces document exceptions, implementations raise them:**

```python
async def generate_response(self, data: Request) -> Response:
    """Generate response.
    
    Raises:
        GenerationException: If generation fails.
        ModelNotFoundException: If model not found.
        ValidationException: If response format invalid.
    """
    ...
```

## Package Exports

```python
# domain/interfaces/__init__.py
"""[Domain] domain interfaces."""

from .{service}_api_repository import {Service}APIRepositoryInterface

__all__ = [
    "{Service}APIRepositoryInterface",
]
```

## Checklist

- [ ] Interface uses `Protocol` from `typing`
- [ ] Filename: `{service}_api_repository.py`
- [ ] Class: `{Service}APIRepositoryInterface`
- [ ] All methods are `async`
- [ ] All methods have complete docstrings
- [ ] All methods have type hints
- [ ] Methods use `...` as body
- [ ] Returns domain value objects (not dicts)
- [ ] Documents domain exceptions
- [ ] No transaction methods
- [ ] No audit parameters
- [ ] Exported in `__init__.py`

## Real-World Example

```python
"""GenAI API repository interface (Port)."""

from typing import Protocol

from ..value_objects import GenaiGeneration, GenaiModel, GenaiResponse


class GenAIAPIRepositoryInterface(Protocol):
    """GenAI API repository protocol interface (Port).
    
    Implementations:
        - RESTGenAIAPIRepository: REST/HTTP implementation
    """
    
    async def get_available_models(self) -> list[GenaiModel]:
        """Get available GenAI models.
        
        Returns:
            List of available models.
            
        Raises:
            GenAIServiceException: If request fails.
            GenAIModelValidationException: If response invalid.
        """
        ...
    
    async def generate_response(
        self,
        generation_data: GenaiGeneration,
    ) -> GenaiResponse:
        """Generate response from GenAI model.
        
        Args:
            generation_data: Generation request data.
            
        Returns:
            Generated response.
            
        Raises:
            GenAIGenerationException: If generation fails.
        """
        ...
    
    async def get_model(self, model_name: str) -> GenaiModel | None:
        """Get model by name.
        
        Args:
            model_name: Name of model to retrieve.
            
        Returns:
            Model if found, None otherwise.
            
        Raises:
            GenAIServiceException: If request fails.
        """
        ...
```

## Comparison: Database vs API Repositories

| Aspect | Database Repositories | API Repositories |
|--------|----------------------|------------------|
| Purpose | Persist entities | Call external services |
| Returns | Entities (with ID) | Value Objects / Models |
| Methods | CRUD operations | Service-specific actions |
| Transactions | `commit()`, `rollback()` | Not applicable |
| Audit | `created_by`, `updated_by` | Not needed |
| Not Found | Return `None` | Return `None` or raise |
| Async | Always async | Always async |

