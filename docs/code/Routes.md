# API Routes (Endpoints)

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **API Routes** | `Presentation Layer` | `Clean Architecture` `DDD` `RESTful API` `FastAPI` |

## Definition

Routes are the presentation layer entry points for the application, handling HTTP requests and responses. They define API endpoints, validate incoming data through schemas, delegate business logic to services, and return properly formatted responses. Routes act as the adapter between HTTP and the domain layer.

**Key Characteristics:**
- **HTTP Request Handling**: Define endpoints with HTTP methods (GET, POST, PUT, PATCH, DELETE)
- **Input Validation**: Use Pydantic schemas for request validation
- **Dependency Injection**: Inject services and dependencies via FastAPI
- **Response Formatting**: Transform domain entities to response schemas
- **Status Code Management**: Return appropriate HTTP status codes
- **Error Handling**: Let error handlers manage exceptions
- **Stateless**: No state between requests
- **Business Logic Free**: Delegate all business logic to services

## Architecture Pattern

```
┌────────────────────────────────────────────────────────────┐
│                    HTTP Request                            │
│          (Client → API Gateway → Route Handler)            │
└───────────────────────┬────────────────────────────────────┘
                        │
┌───────────────────────┴────────────────────────────────────┐
│                 Presentation Layer                         │
│                    (Routes/Handlers)                       │
│   ┌─────────────────────────────────────────────────┐      │
│   │     Route Handler (handle_xxx)                  │      │
│   │  1. Validate request (schemas)                  │      │
│   │  2. Extract dependencies (DI)                   │      │
│   │  3. Call service method                         │      │
│   │  4. Transform to response schema                │      │
│   │  5. Return HTTP response                        │      │
│   └──────────────────────┬──────────────────────────┘      │
└──────────────────────────┼─────────────────────────────────┘
                           │ delegates to
┌──────────────────────────┴─────────────────────────────────┐
│                 Application Layer                          │
│                  (Domain Services)                         │
│   ┌─────────────────────────────────────────────────┐      │
│   │  Service (Business Logic)                       │      │
│   │  - Validates business rules                     │      │
│   │  - Coordinates repositories                     │      │
│   │  - Manages transactions                         │      │
│   │  - Returns domain entities                      │      │
│   └─────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────┘
```

**Request Flow:**
1. **Client** → Sends HTTP request (JSON body, query params, path params)
2. **Route Handler** → Validates request with input schema
3. **FastAPI DI** → Injects services and dependencies
4. **Service Call** → Delegates business logic
5. **Response Schema** → Transforms domain entity to response
6. **HTTP Response** → Returns with appropriate status code

## File & Naming Rules

### Directory Structure

| Element | Rule | Example |
|---------|------|---------|
| **Base Directory** | `routes/` | `app/domains/prompt/routes/` |
| **Resource Directory** | `{resource}/` | `prompt/`, `prompt_version/`, `publish/` |
| **Admin Directory** | `admin/` | `routes/admin/` (administrative operations) |
| **Sub-routes** | `{operation}/` | `update/` (for grouped operations) |

### File Naming

| Pattern | Rule | Example | ❌ Avoid |
|---------|------|---------|----------|
| **CRUD Operations** | `{verb}_{noun}.py` | `create.py`, `delete.py` | `post.py`, `remove.py` |
| **Find Operations** | `find_{criteria}.py` | `find_by_id.py`, `find_by_team.py`, `find_all.py` | `get.py`, `list.py`, `retrieve.py` |
| **Complex Operations** | `{action}_{resource}.py` | `create_iteration.py`, `publish.py` | `iteration.py`, `prod.py` |
| **Update Operations** | `update_{field}.py` | `update_variables.py` | `patch_variables.py`, `set.py` |
| **Admin Operations** | `{resource}_hard_delete.py` | `prompt_hard_delete.py` | `delete_prompt.py` |

### Handler Function Naming

| Pattern | Rule | Example | ❌ Avoid |
|---------|------|---------|----------|
| **All Handlers** | `handle_{operation}` | `handle_create_prompt()` | `create_prompt()`, `create()` |
| **Find Operations** | `handle_find_{criteria}` | `handle_find_by_id()`, `handle_find_all()` | `handle_list()`, `handle_get()` |
| **Update Operations** | `handle_update_{field}` | `handle_update_variables()` | `handle_patch()`, `handle_set()` |
| **Delete Operations** | `handle_delete()` | `handle_delete()` | `handle_remove()`, `handle_destroy()` |

### Router Naming

| Element | Rule | Example |
|---------|------|---------|
| **Router Variable** | `router` | `router = APIRouter()` |
| **Router Import** | `{operation}_router` | `create_router`, `find_all_router` |
| **Grouped Router Import** | `{resource}_router` | `prompt_router`, `prompt_version_router` |

## ⚠️ CRITICAL RULES

### Rule 1: All Routes Must End with Trailing Slash (/)

**ALL route paths MUST end with a trailing slash `/`**. This is a mandatory convention for API consistency.

```python
# ✅ CORRECT - All paths end with /
@router.get(path="/")
@router.get(path="/{prompt_id}/")
@router.post(path="/{prompt_id}/publish/")
@router.patch(path="/{prompt_version_id}/variables/")
@router.delete(path="/prompt/{prompt_id}/hard-delete/")

# ❌ INCORRECT - Missing trailing slash
@router.get(path="/{prompt_id}")           # ❌ Missing /
@router.post(path="/{prompt_id}/publish")  # ❌ Missing /
@router.patch(path="/variables")            # ❌ Missing /
```

**Why this matters:**
- **URL Consistency**: Ensures all API endpoints follow the same pattern
- **Redirect Avoidance**: Prevents automatic redirects from non-slash to slash URLs
- **Client Expectations**: Makes API behavior predictable for consumers
- **Documentation Clarity**: OpenAPI/Swagger docs show consistent patterns

### Rule 2: Avoid Python Reserved Words

**Never use Python reserved words or built-in method names in operation names**, as they can cause:
- Method resolution conflicts
- IDE autocomplete issues
- Runtime interpretation errors
- Shadowing of Python built-ins

### Common Reserved Words to Avoid

| ❌ Avoid | ✅ Use Instead | Reason |
|----------|----------------|--------|
| `list` | `find_all`, `find_by_{criteria}` | Conflicts with Python's `list()` type and `.list()` methods |
| `set` | `update`, `update_{field}` | Conflicts with Python's `set()` type |
| `patch` | `update`, `modify` | Too HTTP-specific, not semantic |
| `get` | `find_by_id`, `find_{criteria}` | Too generic, use semantic names |
| `delete` | ✅ OK for route files | Acceptable in route filenames, but use `handle_delete()` |
| `filter` | `find_by_{criteria}` | Conflicts with Python's `filter()` built-in |
| `map` | `transform`, `convert` | Conflicts with Python's `map()` built-in |
| `type` | `kind`, `category` | Conflicts with Python's `type()` built-in |

### Examples of Good vs Bad Naming

```python
# ❌ BAD - Uses reserved word "list"
# File: list.py or list_all.py
@router.get("/")
async def list_prompts():  # Conflicts with list() method
    pass

# ✅ GOOD - Uses semantic "find_all"
# File: find_all.py
@router.get("/")
async def handle_find_all():  # Clear and semantic
    pass

# ❌ BAD - Uses generic "get"
# File: get.py or get_by_id.py
@router.get("/{id}/")
async def get_prompt():  # Too generic and HTTP-specific
    pass

# ✅ GOOD - Uses semantic "find_by_id"
# File: find_by_id.py
@router.get("/{id}/")
async def handle_find_by_id():  # Clear intent
    pass

# ❌ BAD - Uses reserved word "set"
# File: set_variables.py
@router.patch("/{id}/variables/")
async def set_variables():  # Conflicts with set() type
    pass

# ✅ GOOD - Uses semantic "update"
# File: update_variables.py
@router.patch("/{id}/variables/")
async def handle_update_variables():  # Clear and semantic
    pass
```

## Implementation Rules

### Basic Route Structure

```python
"""[Operation description] route.

This module provides the [operation] endpoint for [resource].
[Additional details about the operation].
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, status
from ulid import ULID

from app.domains.xxx.dependencies import get_xxx_service_dependency
from app.domains.xxx.schemas import (
    OperationRequestSchema,
    OperationResponseSchema,
)
from app.domains.xxx.services import XxxService
from app.shared.dependencies import get_request_by_dependency


router = APIRouter()


@router.{method}(
    path="/{resource_id}/",
    status_code=status.HTTP_XXX_XXX,
    summary="Short operation description",
    description="Detailed operation description",
    response_description="What is returned",
)
async def handle_operation(
    resource_id: Annotated[ULID, Path(description="Resource ID")],
    request: Annotated[OperationRequestSchema, Body()],
    current_user: Annotated[str, Depends(get_request_by_dependency)],
    service: Annotated[XxxService, Depends(get_xxx_service_dependency)],
) -> OperationResponseSchema:
    """Handle [operation] endpoint.
    
    [Detailed docstring explaining what this endpoint does,
    including business logic context and any important notes].
    
    Args:
        resource_id: Unique identifier of the resource.
        request: Request body with operation data.
        current_user: Current authenticated user identifier.
        service: Injected service for business logic.
    
    Returns:
        OperationResponseSchema: Operation result.
    
    Raises:
        ResourceNotFoundException: If resource not found.
        [Other domain exceptions as needed].
    """
    # 1. Extract/transform data if needed
    entity_data = EntityData.model_validate(request)
    
    # 2. Delegate to service
    result = await service.operation(
        resource_id=str(resource_id),
        data=entity_data,
        current_user=current_user,
    )
    
    # 3. Transform to response schema
    return OperationResponseSchema.model_validate(result)
```

### HTTP Method Mapping

| Operation | HTTP Method | Status Code | Response Body |
|-----------|-------------|-------------|---------------|
| **Create** | `POST` | `201 Created` | Created resource |
| **Find (Single)** | `GET` | `200 OK` | Single resource |
| **Find (Multiple)** | `GET` | `200 OK` | List + pagination |
| **Update (Full)** | `PUT` | `200 OK` | Updated resource |
| **Update (Partial)** | `PATCH` | `200 OK` | Updated resource |
| **Delete (Soft)** | `DELETE` | `204 No Content` | Empty (`Response`) |
| **Delete (Hard)** | `DELETE` | `204 No Content` | Empty (`Response`) |

### Router Organization Patterns

#### Pattern 1: Resource-Based Router

```python
"""Prompt resource operations router."""

from fastapi import APIRouter

from .create import router as create_prompt_router
from .delete import router as delete_prompt_router
from .find_all import router as find_all_router
from .find_by_id import router as find_by_id_router

router = APIRouter()

router.include_router(create_prompt_router)
router.include_router(delete_prompt_router)
router.include_router(find_all_router)
router.include_router(find_by_id_router)

__all__ = ["router"]
```

#### Pattern 2: Domain Router with Prefixes

```python
"""Prompt routes package."""

from fastapi import APIRouter

from .prompt import router as prompt_router
from .prompt_version import router as prompt_version_router
from .publish import router as publish_router
from .admin import router as admin_router

router = APIRouter(
    prefix="/prompt",
    tags=["Prompt API"],
)

router.include_router(prompt_router)
router.include_router(prompt_version_router)  # /prompt/version
router.include_router(publish_router)
router.include_router(admin_router)  # /prompt/admin

__all__ = ["router"]
```

#### Pattern 3: Sub-resource Router

```python
"""Prompt version operations router."""

from fastapi import APIRouter

from .create import router as create_router
from .delete import router as delete_router
from .find_by_id import router as find_by_id_router
from .update import router as update_router

router = APIRouter(prefix="/version")  # Adds /version to paths

router.include_router(create_router)
router.include_router(find_by_id_router)
router.include_router(delete_router)
router.include_router(update_router)

__all__ = ["router"]
```

## Route Patterns by Operation

### 1. Create Resource (POST)

```python
"""Prompt create route."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.domain.entities import PromptData
from app.domains.prompt.schemas import (
    CreatePromptSchemaRequest,
    CreatePromptSchemaResponse,
)
from app.domains.prompt.services import PromptService
from app.shared.dependencies import get_request_by_dependency


router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new prompt",
    description="Creates a new prompt with name and description",
)
async def handle_create_prompt(
    request: Annotated[CreatePromptSchemaRequest, Body()],
    current_user: Annotated[str, Depends(get_request_by_dependency)],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> CreatePromptSchemaResponse:
    """Handle create prompt endpoint.
    
    Creates new prompt with primary ownership for the creator.
    
    Args:
        request: Prompt creation data (name, description).
        current_user: Authenticated user identifier.
        service: Prompt service (with ownership management).
    
    Returns:
        Created prompt with ID, name, description, and version.
    """
    prompt_data = PromptData.model_validate(request)
    prompt = await service.create(prompt_data, current_user)
    
    return CreatePromptSchemaResponse.model_validate(prompt)
```

**Key Points:**
- ✅ Status: `201 Created`
- ✅ Path: `/` (for resource creation)
- ✅ Method: `POST`
- ✅ Returns: Complete created resource
- ✅ Validates request via schema
- ✅ Uses `current_user` for audit

### 2. Find Resource by ID (GET)

```python
"""Prompt find by ID route."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from ulid import ULID

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.schemas import FindByIdPromptSchemaResponse
from app.domains.prompt.services import PromptService


router = APIRouter()


@router.get(
    path="/{prompt_id}/",
    status_code=status.HTTP_200_OK,
    summary="Find prompt by ID",
    description="Retrieves complete information about a specific prompt",
)
async def handle_find_by_id(
    prompt_id: Annotated[ULID, Path(description="Prompt ID")],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> FindByIdPromptSchemaResponse:
    """Handle find prompt by ID endpoint.
    
    Retrieves detailed information about a specific prompt identified by its unique ID.
    
    Args:
        prompt_id: Unique identifier of the prompt.
        service: Prompt service dependency.
    
    Returns:
        Complete prompt information.
    
    Raises:
        PromptNotFoundException: If prompt is not found.
    """
    prompt = await service.get_by_id(prompt_id=str(prompt_id))
    return FindByIdPromptSchemaResponse.model_validate(prompt)
```

**Key Points:**
- ✅ Status: `200 OK`
- ✅ Path: `/{resource_id}/`
- ✅ Method: `GET`
- ✅ Returns: Single resource
- ✅ Uses `Path` for route parameters
- ✅ ULID type validation

### 3. Find All Resources with Pagination (GET)

```python
"""Prompt find all route."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.schemas import (
    FindAllPromptSchemaItem,
    FindAllPromptSchemaResponse,
)
from app.domains.prompt.services import PromptService
from app.shared.dependencies.pagination import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas.pagination import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Find all prompts",
    description="Retrieves all prompts with pagination support",
)
async def handle_find_all(
    pagination_request: Annotated[Pagination, Depends(get_pagination_dependency)],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> FindAllPromptSchemaResponse:
    """Handle find all prompts endpoint.
    
    Retrieves all prompts in the system with pagination support.
    
    Args:
        pagination_request: Pagination parameters (page, size).
        service: Prompt service dependency.
    
    Returns:
        Paginated list of all prompts.
    """
    prompts, total = await service.find_all(
        offset=pagination_request.offset,
        limit=pagination_request.limit,
    )
    return FindAllPromptSchemaResponse(
        data=[FindAllPromptSchemaItem.model_validate(prompt) for prompt in prompts],
        pagination=PaginationSchemaData(
            total=total,
            total_per_page=pagination_request.size,
            current_page=pagination_request.page,
        ),
    )
```

**Key Points:**
- ✅ Status: `200 OK`
- ✅ Path: `/` (for collection)
- ✅ Method: `GET`
- ✅ Returns: Array of items + pagination metadata
- ✅ Uses `get_pagination_dependency`
- ✅ Transforms list comprehension for items
- ❌ **NEVER name this `list.py`, `list_all.py` or `handle_list()`** - use `find_all.py` and `handle_find_all()`
- ❌ **NEVER use `get.py` or `get_by_id.py`** - use `find_by_id.py` and `handle_find_by_id()`

### 4. Find Resources by Criteria (GET)

```python
"""Prompt find by team route."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.domain.enums import OwnerType
from app.domains.prompt.schemas import (
    FindByTeamPromptSchemaItem,
    FindByTeamPromptSchemaResponse,
)
from app.domains.prompt.services import PromptService
from app.shared.dependencies.pagination import get_pagination_dependency
from app.shared.domain.value_objects import Pagination
from app.shared.schemas.pagination import PaginationSchemaData


router = APIRouter()


@router.get(
    path="/{team_id}/",
    status_code=status.HTTP_200_OK,
    summary="Find prompts by team",
    description="Find prompts accessible by a team",
)
async def handle_find_by_team(
    team_id: Annotated[str, Path(description="Team ID")],
    pagination_request: Annotated[Pagination, Depends(get_pagination_dependency)],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> FindByTeamPromptSchemaResponse:
    """Find prompts accessible by a team.
    
    Uses prompt_ownership table to find all prompts where team has access.
    
    Args:
        team_id: Team identifier.
        pagination_request: Pagination parameters (page, size).
        service: Prompt service dependency.
    
    Returns:
        Paginated list of prompts accessible by the team.
    """
    prompts, total = await service.find_by_owner(
        owner_type=OwnerType.TEAM,
        owner_id=team_id,
        offset=pagination_request.offset,
        limit=pagination_request.limit,
    )
    return FindByTeamPromptSchemaResponse(
        data=[FindByTeamPromptSchemaItem.model_validate(prompt) for prompt in prompts],
        pagination=PaginationSchemaData(
            total=total,
            total_per_page=pagination_request.size,
            current_page=pagination_request.page,
        ),
    )
```

**Key Points:**
- ✅ Status: `200 OK`
- ✅ Path: `/{criteria_id}/` (specific to filter criteria)
- ✅ Method: `GET`
- ✅ Returns: Filtered array + pagination
- ✅ Clear semantic naming (`find_by_team`, not `list_team`)

### 5. Update Resource (Partial) (PATCH)

```python
"""Update prompt version variables route."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from ulid import ULID

from app.domains.prompt.dependencies import get_prompt_version_service_dependency
from app.domains.prompt.schemas.prompt_version import (
    UpdateVariablesPromptVersionSchemaRequest,
    UpdateVariablesPromptVersionSchemaResponse,
)
from app.domains.prompt.services import PromptVersionService
from app.shared.dependencies import get_request_by_dependency


router = APIRouter()


@router.patch(
    path="/{prompt_version_id}/variables/",
    status_code=status.HTTP_200_OK,
    summary="Update prompt version variables",
    description="Updates the variables configuration of a specific prompt version",
    response_description="Updated prompt version with new variables",
)
async def handle_update_variables(
    prompt_version_id: Annotated[ULID, Path(description="Prompt version ID")],
    service: Annotated[
        PromptVersionService, Depends(get_prompt_version_service_dependency)
    ],
    request: Annotated[UpdateVariablesPromptVersionSchemaRequest, Body()],
    current_user: Annotated[str, Depends(get_request_by_dependency)],
) -> UpdateVariablesPromptVersionSchemaResponse:
    """Handle update prompt version variables endpoint.
    
    This endpoint updates the variables configuration of a specific prompt version
    and returns the complete updated entity.
    
    Args:
        prompt_version_id: Unique identifier of the prompt version to update.
        service: Injected prompt version service for business logic.
        request: Request body with new variables configuration.
        current_user: Current authenticated user identifier from request headers.
    
    Returns:
        UpdateVariablesPromptVersionSchemaResponse: Complete updated version information.
    """
    updated_version = await service.update_variables(
        version_id=str(prompt_version_id),
        variables=request.variables,
        current_user=current_user,
    )
    return UpdateVariablesPromptVersionSchemaResponse.model_validate(updated_version)
```

**Key Points:**
- ✅ Status: `200 OK`
- ✅ Path: `/{resource_id}/{field}/`
- ✅ Method: `PATCH` (partial update)
- ✅ Returns: Complete updated resource
- ✅ Named `update_variables`, **NOT** `patch_variables` or `set_variables`
- ✅ Uses `current_user` for audit

### 6. Delete Resource (Soft Delete) (DELETE)

```python
"""Delete prompt route."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status
from ulid import ULID

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.services import PromptService
from app.shared.dependencies import get_request_by_dependency


router = APIRouter()


@router.delete(
    path="/{prompt_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a prompt by ID",
    description="Soft deletes a specific prompt (marks as deleted)",
    response_description="Prompt successfully deleted",
)
async def handle_delete(
    prompt_id: Annotated[ULID, Path(description="Prompt ID")],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
    current_user: Annotated[str, Depends(get_request_by_dependency)],
) -> Response:
    """Handle delete prompt by ID endpoint.
    
    This endpoint soft deletes a specific prompt (marks it as deleted
    without removing it from the database). Returns 204 No Content on success.
    
    Args:
        prompt_id: Unique identifier of the prompt to delete.
        service: Injected prompt service for business logic.
        current_user: Current authenticated user identifier from request headers.
    
    Returns:
        Response: 204 No Content on successful deletion.
    
    Raises:
        PromptNotFoundException: If prompt not found (handled by error handler).
    """
    await service.delete(prompt_id=str(prompt_id), deleted_by=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

**Key Points:**
- ✅ Status: `204 No Content`
- ✅ Path: `/{resource_id}/`
- ✅ Method: `DELETE`
- ✅ Returns: Empty `Response` object
- ✅ Uses `current_user` for audit
- ✅ Soft delete (marks as deleted, doesn't remove from DB)

### 7. Complex Operation (POST)

```python
"""Publish prompt version route."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from ulid import ULID

from app.domains.prompt.dependencies import get_publish_service_dependency
from app.domains.prompt.schemas.publish import (
    PublishPromptVersionSchemaRequest,
    PublishPromptVersionSchemaResponse,
)
from app.domains.prompt.services import PublishService
from app.shared.dependencies import get_request_by_dependency


router = APIRouter()


@router.post(
    path="/{prompt_version_id}/publish/",
    status_code=status.HTTP_201_CREATED,
    summary="Publish a prompt version to production",
    description="Promotes a development version to production with semantic version increment",
    response_description="Successfully published version information",
)
async def handle_publish(
    prompt_version_id: Annotated[ULID, Path(description="Prompt version ID")],
    request: Annotated[PublishPromptVersionSchemaRequest, Body()],
    service: Annotated[PublishService, Depends(get_publish_service_dependency)],
    current_user: Annotated[str, Depends(get_request_by_dependency)],
) -> PublishPromptVersionSchemaResponse:
    """Handle publish prompt version endpoint.
    
    This endpoint promotes a development prompt version to production by:
    1. Validating the development version exists
    2. Checking version conflicts (source_version must match current_version)
    3. Computing the next semantic version based on increment type
    4. Creating a new prompt history record
    5. Updating the prompt with the new production data
    
    Args:
        prompt_version_id: ID of the development version to publish.
        request: Publish request with version increment type.
        service: Injected publish service.
        current_user: Current user ID from headers.
    
    Returns:
        PublishPromptVersionSchemaResponse: Success response with created history and new version.
    
    Raises:
        PromptVersionNotFoundException: If version not found (handled by error handler).
        PromptNotFoundException: If prompt not found (handled by error handler).
        VersionConflictError: If version conflict detected (handled by error handler).
        InvalidVersionTypeError: If invalid version type (handled by error handler).
    """
    prompt_history = await service.publish_version(
        prompt_version_id=str(prompt_version_id),
        version_type=request.version_type.value,
        current_user=current_user,
    )
    
    return PublishPromptVersionSchemaResponse(
        message=f"Prompt version successfully published as version {prompt_history.version}",
        history_id=str(prompt_history.id),
        prompt_id=str(prompt_history.prompt_id),
        version=prompt_history.version or "1.0.0",
        name=prompt_history.name,
        ai_description=prompt_history.ai_description,
        system_prompt=prompt_history.system_prompt,
        user_prompt=prompt_history.user_prompt,
        variables=prompt_history.variables,
        llm_configuration=prompt_history.llm_configuration,
        created_at=prompt_history.created_at,
        created_by=prompt_history.created_by,
    )
```

**Key Points:**
- ✅ Status: `201 Created` (creates new resource - prompt history)
- ✅ Path: `/{resource_id}/{operation}/`
- ✅ Method: `POST` (complex state-changing operation)
- ✅ Returns: Operation result with detailed information
- ✅ Detailed docstring with step-by-step explanation
- ✅ All possible exceptions documented

### 8. Create Iteration/Copy (POST)

```python
"""Prompt version iteration route."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, status
from ulid import ULID

from app.domains.prompt.dependencies import get_prompt_version_service_dependency
from app.domains.prompt.domain.entities import PromptVersionData
from app.domains.prompt.schemas import (
    CreateIterationPromptVersionSchemaRequest,
    CreateIterationPromptVersionSchemaResponse,
)
from app.domains.prompt.services import PromptVersionService
from app.shared.dependencies import get_request_by_dependency


router = APIRouter()


@router.post(
    path="/{prompt_version_id}/iteration/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new iteration from existing version",
    description="Creates a new version by copying an existing one and incrementing the iteration counter",
    response_description="Created iteration with incremented number",
)
async def handle_create_iteration(
    prompt_version_id: Annotated[ULID, Path(description="Prompt version ID")],
    service: Annotated[
        PromptVersionService, Depends(get_prompt_version_service_dependency)
    ],
    request: Annotated[CreateIterationPromptVersionSchemaRequest, Body()],
    current_user: Annotated[str, Depends(get_request_by_dependency)],
) -> CreateIterationPromptVersionSchemaResponse:
    """Handle create iteration endpoint.
    
    This endpoint creates a new development version by copying all values from
    the specified version and incrementing the iteration counter. The new version
    will have the same prompt_id, source_version, and all configuration values,
    but with a new comment and incremented iteration number.
    
    Args:
        prompt_version_id: ID of the version to create iteration from.
        service: Injected prompt version service for business logic.
        request: Request body with iteration comment.
        current_user: Current authenticated user identifier from request headers.
    
    Returns:
        CreateIterationPromptVersionSchemaResponse: Created iteration information.
    
    Raises:
        PromptVersionNotFoundException: If the source version is not found.
    """
    existing_version = await service.get_by_id(prompt_version_id=str(prompt_version_id))
    prompt_version_data = PromptVersionData.model_validate(existing_version)
    prompt_version_data.comment = request.comment
    prompt_version = await service.create_iteration(
        entity=prompt_version_data, current_user=current_user
    )
    return CreateIterationPromptVersionSchemaResponse.model_validate(prompt_version)
```

**Key Points:**
- ✅ Status: `201 Created`
- ✅ Path: `/{resource_id}/iteration/`
- ✅ Method: `POST` (creates new resource from existing)
- ✅ Returns: Newly created iteration
- ✅ Clear explanation of copy-and-increment behavior

### 9. Admin Hard Delete (DELETE)

```python
"""Hard delete prompt route for administrative purposes.

This module provides administrative endpoints for permanently deleting prompts
from the database. These operations bypass soft-delete mechanisms and should
be used with extreme caution.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status
from ulid import ULID

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.services import PromptService
from app.shared.dependencies import get_request_by_dependency


router = APIRouter()


@router.delete(
    path="/prompt/{prompt_id}/hard-delete/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="[ADMIN] Permanently delete a prompt",
    description=(
        "**WARNING**: Permanently deletes a prompt from the database. "
        "This operation cannot be undone and will remove all data associated "
        "with the prompt. Use with extreme caution. "
        "This endpoint is intended for administrative purposes only, such as "
        "test data cleanup or data purging operations."
    ),
    response_description="Prompt permanently deleted",
)
async def handle_prompt_hard_delete(
    prompt_id: Annotated[ULID, Path(description="Prompt ID to permanently delete")],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
    current_user: Annotated[str, Depends(get_request_by_dependency)],
) -> Response:
    """Handle prompt hard delete endpoint.
    
    This endpoint permanently deletes a prompt from the database, bypassing
    soft-delete mechanisms. The operation is irreversible and will remove
    all associated data.
    
    **Use Cases**:
    - Test data cleanup in non-production environments
    - Administrative data purging operations
    - Compliance with data deletion requirements
    
    Args:
        prompt_id: Unique identifier of the prompt to permanently delete.
        service: Injected prompt service for business logic.
        current_user: Current authenticated user identifier from request headers.
    
    Returns:
        Response: 204 No Content on successful deletion.
    
    Raises:
        PromptNotFoundException: If prompt not found (handled by error handler).
    """
    await service.hard_delete(prompt_id=str(prompt_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

**Key Points:**
- ✅ Status: `204 No Content`
- ✅ Path: `/prompt/{resource_id}/hard-delete/` (admin prefix added by router)
- ✅ Method: `DELETE`
- ✅ Returns: Empty `Response` object
- ✅ `[ADMIN]` tag in summary
- ✅ **WARNING** in description
- ✅ Clear use cases documented
- ✅ Permanent deletion (removes from DB)

## Dependency Injection Patterns

### Service Dependencies

```python
from typing import Annotated
from fastapi import Depends

from app.domains.prompt.dependencies import get_prompt_service_dependency
from app.domains.prompt.services import PromptService

async def handle_operation(
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> ResponseSchema:
    """Handler with service dependency injection."""
    result = await service.operation()
    return ResponseSchema.model_validate(result)
```

### Current User (Authentication)

```python
from typing import Annotated
from fastapi import Depends

from app.shared.dependencies import get_request_by_dependency

async def handle_operation(
    current_user: Annotated[str, Depends(get_request_by_dependency)],
) -> ResponseSchema:
    """Handler with current user from request headers."""
    result = await service.create(created_by=current_user)
    return ResponseSchema.model_validate(result)
```

### Pagination

```python
from typing import Annotated
from fastapi import Depends

from app.shared.dependencies.pagination import get_pagination_dependency
from app.shared.domain.value_objects import Pagination

async def handle_find_all(
    pagination_request: Annotated[Pagination, Depends(get_pagination_dependency)],
) -> ResponseSchema:
    """Handler with pagination dependency."""
    results, total = await service.find_all(
        offset=pagination_request.offset,
        limit=pagination_request.limit,
    )
    return ResponseSchema(
        data=[Item.model_validate(r) for r in results],
        pagination=PaginationSchemaData(
            total=total,
            total_per_page=pagination_request.size,
            current_page=pagination_request.page,
        ),
    )
```

## Parameter Patterns

### Path Parameters

```python
from typing import Annotated
from fastapi import Path
from ulid import ULID

async def handle_operation(
    resource_id: Annotated[ULID, Path(description="Resource ID")],
    team_id: Annotated[str, Path(description="Team identifier")],
) -> ResponseSchema:
    """Handler with path parameters."""
    result = await service.get_by_id(resource_id=str(resource_id))
    return ResponseSchema.model_validate(result)
```

**Path Parameter Rules:**
- ✅ Use `Annotated` with type and `Path()` descriptor
- ✅ Convert ULID to string before passing to service
- ✅ Always provide description in `Path()`
- ✅ Use descriptive parameter names (not just `id`)

### Query Parameters

```python
from typing import Annotated
from fastapi import Query

async def handle_search(
    query: Annotated[str | None, Query(description="Search query")] = None,
    status: Annotated[str | None, Query(description="Filter by status")] = None,
) -> ResponseSchema:
    """Handler with query parameters."""
    results = await service.search(query=query, status=status)
    return ResponseSchema.model_validate(results)
```

### Request Body

```python
from typing import Annotated
from fastapi import Body

async def handle_create(
    request: Annotated[CreateSchemaRequest, Body()],
) -> CreateSchemaResponse:
    """Handler with request body validation."""
    entity_data = EntityData.model_validate(request)
    result = await service.create(entity_data)
    return CreateSchemaResponse.model_validate(result)
```

## Response Patterns

### Success Response with Data

```python
@router.get("/", status_code=status.HTTP_200_OK)
async def handle_find_all() -> FindAllSchemaResponse:
    """Returns data with 200 OK."""
    results = await service.find_all()
    return FindAllSchemaResponse(data=results)
```

### Created Response

```python
@router.post("/", status_code=status.HTTP_201_CREATED)
async def handle_create(request: CreateRequest) -> CreateResponse:
    """Returns created resource with 201 Created."""
    result = await service.create(request)
    return CreateResponse.model_validate(result)
```

### No Content Response

```python
from fastapi import Response

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def handle_delete(resource_id: ULID) -> Response:
    """Returns empty response with 204 No Content."""
    await service.delete(resource_id=str(resource_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

## Import Patterns

### Standard Route Imports

```python
"""Route module docstring."""

# Standard library
from typing import Annotated

# FastAPI framework
from fastapi import APIRouter, Body, Depends, Path, Query, Response, status

# Third-party (if needed)
from ulid import ULID

# Domain dependencies
from app.domains.xxx.dependencies import get_xxx_service_dependency

# Domain entities (for data transformation)
from app.domains.xxx.domain.entities import EntityData

# Domain schemas (request/response)
from app.domains.xxx.schemas import (
    OperationRequestSchema,
    OperationResponseSchema,
)

# Domain services
from app.domains.xxx.services import XxxService

# Shared dependencies
from app.shared.dependencies import get_request_by_dependency
from app.shared.dependencies.pagination import get_pagination_dependency

# Shared domain (if needed)
from app.shared.domain.value_objects import Pagination

# Shared schemas (if needed)
from app.shared.schemas.pagination import PaginationSchemaData
```

### Router Module Imports (`__init__.py`)

```python
"""Router package initialization."""

from fastapi import APIRouter

from .create import router as create_router
from .delete import router as delete_router
from .find_all import router as find_all_router
from .find_by_id import router as find_by_id_router

router = APIRouter()

router.include_router(create_router)
router.include_router(delete_router)
router.include_router(find_all_router)
router.include_router(find_by_id_router)

__all__ = ["router"]
```

## Error Handling

Routes **should not** handle errors directly. All domain exceptions are caught and handled by global error handlers registered in `app/core/errors/handlers.py`.

### Raise Domain Exceptions in Services

```python
# In service layer
class PromptService:
    async def get_by_id(self, prompt_id: str) -> Prompt:
        prompt = await self.repository.get_by_id(prompt_id)
        if not prompt:
            raise PromptNotFoundException(prompt_id=prompt_id)  # Handled globally
        return prompt
```

### Document Exceptions in Route Docstring

```python
@router.get("/{prompt_id}/")
async def handle_find_by_id(
    prompt_id: Annotated[ULID, Path(description="Prompt ID")],
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> FindByIdPromptSchemaResponse:
    """Handle find prompt by ID endpoint.
    
    Args:
        prompt_id: Unique identifier of the prompt.
        service: Prompt service dependency.
    
    Returns:
        Complete prompt information.
    
    Raises:
        PromptNotFoundException: If prompt is not found.
    """
    prompt = await service.get_by_id(prompt_id=str(prompt_id))
    return FindByIdPromptSchemaResponse.model_validate(prompt)
```

### No Try-Except in Routes

```python
# ❌ BAD - Don't handle exceptions in routes
@router.get("/{prompt_id}/")
async def handle_find_by_id(prompt_id: ULID) -> FindByIdResponse:
    try:
        prompt = await service.get_by_id(prompt_id=str(prompt_id))
        return FindByIdResponse.model_validate(prompt)
    except PromptNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))  # ❌ Don't do this

# ✅ GOOD - Let global error handler manage it
@router.get("/{prompt_id}/")
async def handle_find_by_id(prompt_id: ULID) -> FindByIdResponse:
    prompt = await service.get_by_id(prompt_id=str(prompt_id))  # Exception auto-handled
    return FindByIdResponse.model_validate(prompt)
```

## Schema Validation

### Request Validation

FastAPI automatically validates request data using Pydantic schemas:

```python
from pydantic import BaseModel, Field

class CreatePromptSchemaRequest(BaseModel):
    """Request schema for creating prompts."""
    name: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(None, max_length=500)

@router.post("/")
async def handle_create(
    request: Annotated[CreatePromptSchemaRequest, Body()],  # Auto-validated
) -> CreatePromptSchemaResponse:
    """Validation happens automatically before handler execution."""
    # If we reach here, request is valid
    result = await service.create(request)
    return CreatePromptSchemaResponse.model_validate(result)
```

### Response Validation

```python
@router.get("/{prompt_id}/")
async def handle_find_by_id(
    prompt_id: ULID,
) -> FindByIdPromptSchemaResponse:  # Return type enforces schema
    """Response is validated automatically."""
    prompt = await service.get_by_id(prompt_id=str(prompt_id))
    
    # Transform domain entity to response schema
    return FindByIdPromptSchemaResponse.model_validate(prompt)
```

## Best Practices

### ✅ DO

1. **Always end paths with trailing slash** (`/`, `/{id}/`, `/{id}/operation/`)
2. **Use semantic operation names** (`find_all`, `find_by_id`, `update_variables`)
3. **Prefix handlers with `handle_`** (`handle_create_prompt()`)
4. **Return appropriate HTTP status codes** (`201 Created`, `204 No Content`)
5. **Use dependency injection** for services and utilities
6. **Transform domain entities to response schemas** using `model_validate()`
7. **Document all exceptions** in docstrings
8. **Use `Annotated` for all parameters** with type hints and descriptors
9. **Convert ULID to string** before passing to services
10. **Use `Response` class** for `204 No Content` endpoints
11. **Keep routes thin** - delegate all business logic to services
12. **Use pagination for list endpoints**
13. **Include comprehensive OpenAPI metadata** (summary, description, response_description)

### ❌ DON'T

1. **Never omit trailing slash** - all paths must end with `/`
2. **Never use Python reserved words** (`list`, `set`, `patch`, `filter`)
3. **Don't implement business logic in routes** - delegate to services
4. **Don't handle exceptions in routes** - use global error handlers
5. **Don't use generic names** (`get`, `post`, `fetch`)
6. **Don't skip type annotations** - always use `Annotated`
7. **Don't forget audit fields** (`current_user`, `created_by`, `updated_by`)
8. **Don't return domain entities directly** - transform to response schemas
9. **Don't use raw dictionaries** - use Pydantic models
10. **Don't hardcode status codes** - use `status.HTTP_*` constants
11. **Don't skip docstrings** - document all handlers thoroughly

## Checklist for New Routes

- [ ] **Path ends with trailing slash** (e.g., `/`, `/{id}/`, `/{id}/operation/`)
- [ ] **File named semantically** (e.g., `find_by_id.py`, not `get.py` or `list.py`)
- [ ] **Handler named with `handle_` prefix** (e.g., `handle_find_by_id()`)
- [ ] **Module docstring** present and descriptive
- [ ] **Correct HTTP method** (`GET`, `POST`, `PATCH`, `DELETE`)
- [ ] **Appropriate status code** (`200 OK`, `201 Created`, `204 No Content`)
- [ ] **OpenAPI metadata** (summary, description, response_description)
- [ ] **Type annotations** with `Annotated` for all parameters
- [ ] **Dependency injection** for service and current_user
- [ ] **Request validation** via schema (if applicable)
- [ ] **Response schema** transformation via `model_validate()`
- [ ] **Comprehensive docstring** with Args, Returns, Raises
- [ ] **ULID converted to string** before service call
- [ ] **Pagination** for list endpoints
- [ ] **Audit fields** passed to service (`current_user`)
- [ ] **Router included** in `__init__.py`
- [ ] **No business logic** in route (all in service)
- [ ] **No exception handling** (rely on global handlers)
- [ ] **No reserved words** used in operation names

## Common Mistakes

### Mistake 1: Missing Trailing Slash

```python
# ❌ BAD - Missing trailing slash
@router.get(path="/{prompt_id}")
async def handle_find_by_id(prompt_id: ULID) -> FindByIdResponse:
    pass

@router.post(path="/{prompt_id}/publish")
async def handle_publish(prompt_id: ULID) -> PublishResponse:
    pass

# ✅ GOOD - All paths end with /
@router.get(path="/{prompt_id}/")
async def handle_find_by_id(prompt_id: ULID) -> FindByIdResponse:
    pass

@router.post(path="/{prompt_id}/publish/")
async def handle_publish(prompt_id: ULID) -> PublishResponse:
    pass
```

### Mistake 2: Using Reserved Words

```python
# ❌ BAD - Using "list" (Python reserved word)
# File: list.py or list_restaurants.py
@router.get("/")
async def list_restaurants():  # Conflicts with Python's list()
    pass

# ❌ BAD - Using "get" (too generic, HTTP-specific)
# File: get.py or get_restaurant.py
@router.get("/{id}/")
async def get_restaurant():  # Too generic
    pass

# ✅ GOOD - Using semantic "find_all"
# File: find_all.py
@router.get("/")
async def handle_find_all():  # Clear and semantic
    pass

# ✅ GOOD - Using semantic "find_by_id"
# File: find_by_id.py
@router.get("/{id}/")
async def handle_find_by_id():  # Clear intent
    pass
```

### Mistake 3: Business Logic in Routes

```python
# ❌ BAD
@router.post("/")
async def handle_create(request: CreateRequest) -> CreateResponse:
    # Business logic should NOT be here
    if not request.name:
        raise ValueError("Name required")
    prompt = Prompt(name=request.name, version="0.0.0")
    await repository.save(prompt)
    return CreateResponse.model_validate(prompt)

# ✅ GOOD
@router.post("/")
async def handle_create(
    request: CreateRequest,
    service: Annotated[PromptService, Depends(get_prompt_service_dependency)],
) -> CreateResponse:
    # Delegate to service
    entity_data = PromptData.model_validate(request)
    prompt = await service.create(entity_data, current_user)
    return CreateResponse.model_validate(prompt)
```

### Mistake 4: Handling Exceptions in Routes

```python
# ❌ BAD
@router.get("/{prompt_id}/")
async def handle_find_by_id(prompt_id: ULID) -> FindByIdResponse:
    try:
        prompt = await service.get_by_id(prompt_id=str(prompt_id))
        return FindByIdResponse.model_validate(prompt)
    except PromptNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

# ✅ GOOD
@router.get("/{prompt_id}/")
async def handle_find_by_id(prompt_id: ULID) -> FindByIdResponse:
    prompt = await service.get_by_id(prompt_id=str(prompt_id))
    return FindByIdResponse.model_validate(prompt)  # Let global handler manage exceptions
```

### Mistake 5: Not Converting ULID to String

```python
# ❌ BAD
@router.get("/{prompt_id}/")
async def handle_find_by_id(prompt_id: ULID) -> FindByIdResponse:
    prompt = await service.get_by_id(prompt_id=prompt_id)  # ULID object, not string

# ✅ GOOD
@router.get("/{prompt_id}/")
async def handle_find_by_id(prompt_id: ULID) -> FindByIdResponse:
    prompt = await service.get_by_id(prompt_id=str(prompt_id))  # Convert to string
```

### Mistake 6: Forgetting Audit Fields

```python
# ❌ BAD
@router.post("/")
async def handle_create(request: CreateRequest) -> CreateResponse:
    prompt = await service.create(request)  # Missing created_by

# ✅ GOOD
@router.post("/")
async def handle_create(
    request: CreateRequest,
    current_user: Annotated[str, Depends(get_request_by_dependency)],
) -> CreateResponse:
    entity_data = PromptData.model_validate(request)
    prompt = await service.create(entity_data, current_user)  # Include current_user
```

### Mistake 7: Wrong Status Code for Delete

```python
# ❌ BAD
@router.delete("/{prompt_id}/", status_code=status.HTTP_200_OK)
async def handle_delete(prompt_id: ULID) -> dict:
    await service.delete(prompt_id=str(prompt_id))
    return {"message": "Deleted"}  # ❌ Should return 204 No Content

# ✅ GOOD
@router.delete("/{prompt_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def handle_delete(prompt_id: ULID) -> Response:
    await service.delete(prompt_id=str(prompt_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # ✅ Correct
```

---

## Summary

Routes are the **presentation layer** of the application, responsible for:
- Defining RESTful API endpoints
- Validating requests via schemas
- Delegating business logic to services
- Transforming responses to client format
- Managing HTTP concerns (status codes, headers)

**Golden Rules:**
1. ✅ **Always end paths with trailing slash** (`/`, `/{id}/`, `/{id}/operation/`)
2. ✅ Use **semantic operation names** - avoid Python reserved words (`list`, `set`, `patch`)
3. ✅ Keep routes **thin** - all business logic in services
4. ✅ Use **dependency injection** for services and utilities
5. ✅ **Transform** domain entities to response schemas
6. ✅ Let **global error handlers** manage exceptions
7. ✅ Include **comprehensive documentation** (docstrings, OpenAPI metadata)
8. ✅ Follow **RESTful conventions** (HTTP methods, status codes, resource paths)

