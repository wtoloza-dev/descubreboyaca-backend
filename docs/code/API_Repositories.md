# API Repositories

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **API Repositories** | `Domain + Infrastructure Layers` | `Hexagonal Architecture` `Adapters` `REST` |

## Definition

API Repositories are implementations (adapters) that connect domain interfaces to external services via HTTP/REST. They handle HTTP communication, response validation, and error handling while implementing domain-defined protocols.

## Pattern

**API Repository = Interface (Port) + REST Implementation (Adapter) + HTTP Client**

```
Domain Logic → Interface (Port) → REST Adapter → HTTP Client → External Service
```

## Quick Decision Tree

```
Need to interact with external service?
├─ YES → Create API Repository Interface + Implementation
└─ NO  → Use direct HTTP client or SDK
```

## File Structure & Naming

```
app/domains/{domain}/
├── domain/
│   └── interfaces/
│       └── {service}_api_repository.py      # Interface (Protocol)
├── repositories/
│   ├── __init__.py
│   └── rest.py                              # Implementation
└── dependencies/
    └── {service}.py                         # Dependency injection
```

| Element | Rule | Example |
|---------|------|---------|
| Interface File | `domain/interfaces/{service}_api_repository.py` | `domain/interfaces/genai_api_repository.py` |
| Implementation File | `repositories/rest.py` | `repositories/rest.py` |
| Interface Class | `{Service}APIRepositoryInterface` | `GenAIAPIRepositoryInterface` |
| Implementation Class | `REST{Service}APIRepository` | `RESTGenAIAPIRepository` |
| Dependency File | `dependencies/{service}.py` | `dependencies/genai.py` |

## Implementation Rules

### Interface Template (Protocol)

```python
"""[Service] API repository interface (Port).

This module defines the repository protocol (port) for [Service] API operations,
following the hexagonal architecture pattern.
"""

from typing import Protocol

from ..value_objects import ServiceRequest, ServiceResponse


class ServiceAPIRepositoryInterface(Protocol):
    """[Service] API repository protocol interface (Port).
    
    This protocol defines the contract for [Service] API repository implementations.
    
    Implementations:
        - RESTServiceAPIRepository: REST/HTTP implementation
    """
    
    async def get_items(self) -> list[ServiceItem]:
        """Get items from external service.
        
        Returns:
            List of service items.
            
        Raises:
            ServiceException: If the request fails.
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

**Key Points:**
- Use `Protocol` from `typing` (NOT `ABC`)
- All methods end with `...` (NOT `pass`)
- Methods ordered: List/Query → Actions → Single items

### Implementation Template (Adapter)

```python
"""REST [Service] API repository implementation (Adapter).

This module implements the [Service] API repository using REST API calls.
"""

from app.clients.http_client import HTTPClient
from app.core.settings import settings
from app.domains.{domain}.domain.exceptions import ServiceException
from app.domains.{domain}.domain.value_objects import (
    ServiceRequest,
    ServiceResponse,
)


class RESTServiceAPIRepository:
    """REST implementation of [Service] API repository (Adapter).
    
    Attributes:
        http_client: Async HTTP client for external API calls.
    """
    
    def __init__(self, http_client: HTTPClient) -> None:
        """Initialize the REST repository.
        
        Args:
            http_client: Async HTTP client for external API calls.
        """
        self.http_client: HTTPClient = http_client
    
    async def get_items(self) -> list[ServiceItem]:
        """Get items from external service via REST API.
        
        Returns:
            List of service items.
            
        Raises:
            ServiceException: If the API request fails.
        """
        url = f"{settings.SERVICE_BASE_URL}/api/v1/items"
        
        response = await self.http_client.get(url)
        
        if response.status_code != 200:
            raise ServiceException(
                reason=f"HTTP {response.status_code} - Failed to fetch items",
                context={"status_code": response.status_code},
            )
        
        items_data = response.json()
        return [ServiceItem.model_validate(item) for item in items_data]
    
    async def perform_action(
        self,
        request: ServiceRequest,
    ) -> ServiceResponse:
        """Perform action via REST API.
        
        Args:
            request: Request data for the action.
            
        Returns:
            Service response.
            
        Raises:
            ServiceException: If the API request fails.
        """
        url = f"{settings.SERVICE_BASE_URL}/api/v1/actions"
        
        body = request.model_dump(mode="json")
        
        response = await self.http_client.post(url, json=body)
        
        if response.status_code != 200:
            raise ServiceException(
                reason=f"HTTP {response.status_code} - Action failed",
                context={
                    "status_code": response.status_code,
                    "request_body": body,
                },
            )
        
        return ServiceResponse.model_validate(response.json())
    
    async def get_item(self, item_id: str) -> ServiceItem | None:
        """Get specific item by ID.
        
        Args:
            item_id: Item identifier.
            
        Returns:
            Item if found, None otherwise.
            
        Raises:
            ServiceException: If the API request fails.
        """
        url = f"{settings.SERVICE_BASE_URL}/api/v1/items/{item_id}"
        
        response = await self.http_client.get(url)
        
        # Return None for 404
        if response.status_code == 404:
            return None
        
        if response.status_code != 200:
            raise ServiceException(
                reason=f"HTTP {response.status_code} - Failed to fetch item",
                context={"item_id": item_id, "status_code": response.status_code},
            )
        
        return ServiceItem.model_validate(response.json())
```

**Key Points:**
- HTTP client injected via `__init__` (NOT created inside)
- All methods are `async`
- Validate responses with Pydantic: `Model.model_validate()`
- Use `model_dump(mode="json")` for request bodies
- Handle HTTP status codes explicitly
- Return `None` for 404, raise exceptions for other errors

## HTTP Status Code Handling

| Status | Action | Example |
|--------|--------|---------|
| **200/201** | Parse & return | `return Model.model_validate(response.json())` |
| **204** | Return True/None | `return True` |
| **400** | Raise ValidationException | `raise ValidationException(...)` |
| **401** | Raise UnauthorizedException | `raise UnauthorizedException(...)` |
| **404** | Return None/False | `return None` |
| **429** | Raise RateLimitException | `raise RateLimitException(...)` |
| **500+** | Raise ServiceException | `raise ServiceException(...)` |

## Dependency Injection Template

```python
"""[Service] API repository dependencies."""

from typing import Annotated

from fastapi import Depends

from app.clients.http_client import HTTPClient
from app.clients.http_client.dependencies import get_http_client
from app.domains.{domain}.domain.interfaces import ServiceAPIRepositoryInterface
from app.domains.{domain}.repositories.rest import RESTServiceAPIRepository


async def get_service_repository(
    http_client: Annotated[HTTPClient, Depends(get_http_client)],
) -> ServiceAPIRepositoryInterface:
    """Get [Service] API repository instance.
    
    Args:
        http_client: Injected async HTTP client.
        
    Returns:
        [Service] API repository implementation.
    """
    return RESTServiceAPIRepository(http_client=http_client)
```

## Common Patterns

### GET Single Resource
```python
async def get_item(self, item_id: str) -> ServiceItem | None:
    url = f"{settings.BASE_URL}/items/{item_id}"
    response = await self.http_client.get(url)
    
    if response.status_code == 404:
        return None
    
    if response.status_code != 200:
        raise ServiceException(...)
    
    return ServiceItem.model_validate(response.json())
```

### POST Create Resource
```python
async def create_item(self, item_data: ItemData) -> Item:
    url = f"{settings.BASE_URL}/items"
    body = item_data.model_dump(mode="json", exclude_none=True)
    response = await self.http_client.post(url, json=body)
    
    if response.status_code not in (200, 201):
        raise ServiceException(...)
    
    return Item.model_validate(response.json())
```

### GET with Query Parameters
```python
async def search_items(
    self,
    query: str,
    filters: dict[str, Any] | None = None,
) -> list[Item]:
    url = f"{settings.BASE_URL}/items/search"
    params = {"q": query}
    if filters:
        params.update(filters)
    
    response = await self.http_client.get(url, params=params)
    
    if response.status_code != 200:
        raise ServiceException(...)
    
    items_data = response.json()
    return [Item.model_validate(item) for item in items_data]
```

### With Authentication Headers
```python
async def get_protected_resource(self, resource_id: str) -> Resource:
    url = f"{settings.BASE_URL}/resources/{resource_id}"
    headers = {
        "Authorization": f"Bearer {settings.API_TOKEN}",
        "X-API-Key": settings.API_KEY,
    }
    
    response = await self.http_client.get(url, headers=headers)
    
    if response.status_code == 401:
        raise UnauthorizedException(...)
    
    if response.status_code != 200:
        raise ServiceException(...)
    
    return Resource.model_validate(response.json())
```

## Common Mistakes to Avoid

| ❌ DON'T | ✅ DO |
|---------|-------|
| `class Repo(ABC):` | `class RepoInterface(Protocol):` |
| `def get_items():` | `async def get_items():` |
| `return response.json()` | `return Item.model_validate(response.json())` |
| `self.http_client = HTTPClient()` | `def __init__(self, http_client: HTTPClient):` |
| `body = generation_data.dict()` | `body = generation_data.model_dump(mode="json")` |
| `url = "https://api.example.com"` | `url = f"{settings.BASE_URL}"` |
| No status code checking | Check and handle all status codes |
| Silent exception catching | Raise domain exceptions with context |

## Package Exports

### Interface Package
```python
"""[Domain] domain interfaces."""

from .service_api_repository import ServiceAPIRepositoryInterface

__all__ = [
    "ServiceAPIRepositoryInterface",
]
```

### Repository Package
```python
"""[Domain] repository implementations."""

from .rest import RESTServiceAPIRepository

__all__ = [
    "RESTServiceAPIRepository",
]
```

## Checklist

**Interface (Protocol):**
- [ ] Uses `Protocol` (not `ABC`)
- [ ] All methods are `async`
- [ ] All methods use `...` (not `pass`)
- [ ] Complete docstrings with Args/Returns/Raises
- [ ] Returns domain objects (not dicts)
- [ ] No transaction methods (commit/rollback)
- [ ] No audit parameters (created_by, updated_by)
- [ ] Exported in `__init__.py`

**Implementation (Adapter):**
- [ ] HTTP client injected in `__init__`
- [ ] All HTTP methods are `async` with `await`
- [ ] Responses validated with Pydantic
- [ ] HTTP errors handled with domain exceptions
- [ ] 404 returns `None` or `False`
- [ ] Base URLs from settings
- [ ] Request bodies use `model_dump(mode="json")`
- [ ] Complete docstrings
- [ ] Exported in `__init__.py`

**Dependency Injection:**
- [ ] Created in `dependencies/{service}.py`
- [ ] Function is `async`
- [ ] HTTP client injected via `Depends`
- [ ] Returns interface type annotation

