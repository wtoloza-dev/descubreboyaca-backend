# API Schemas (DTOs)

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **API Schemas (DTOs)** | `Presentation Layer` | `Clean Architecture` `DTO Pattern` `REST API` |

## Definition

API Schemas (also known as DTOs - Data Transfer Objects) are Pydantic models that define the structure of HTTP request and response payloads. They serve as the contract between the client and the API, providing validation, serialization, and documentation. Schemas live in the Presentation Layer and should mirror the route structure for clarity and maintainability.

**Key Characteristics:**
- **HTTP Contract**: Define API request/response structure
- **Validation**: Enforce input validation rules
- **Documentation**: Auto-generate OpenAPI/Swagger docs
- **Serialization**: Convert between JSON and Python objects
- **Type Safety**: Provide type hints for IDE and static analysis
- **Route-Specific**: One schema file per route operation
- **Entity Conversion**: Convert to/from domain entities

## Schema Pattern Overview

```
┌──────────────────────────────────────────────────────────┐
│                     Client (HTTP)                        │
│                   JSON Request/Response                  │
└────────────────────┬─────────────────────────────────────┘
                     │ HTTP
┌────────────────────┴─────────────────────────────────────┐
│                  Presentation Layer                      │
│  ┌────────────────────────────────────────────────┐      │
│  │           Routes (FastAPI)                     │      │
│  │  - Receive: {Operation}{Entity}SchemaRequest   │      │
│  │  - Return:  {Operation}{Entity}SchemaResponse  │      │
│  └─────────────┬──────────────────────────────────┘      │
│                │ validates & converts                    │
│  ┌─────────────┴──────────────────────────────────┐      │
│  │         API Schemas (DTOs)                     │      │
│  │  - Request schemas  (input validation)         │      │
│  │  - Response schemas (output serialization)     │      │
│  │  - Item schemas     (list elements)            │      │
│  └─────────────┬──────────────────────────────────┘      │
└────────────────┼─────────────────────────────────────────┘
                 │ converts to/from
┌────────────────┴─────────────────────────────────────────┐
│                  Application Layer                       │
│  ┌────────────────────────────────────────────────┐      │
│  │         Domain Entities                        │      │
│  │  - PromptData (for creation)                   │      │
│  │  - Prompt (for response)                       │      │
│  └────────────────────────────────────────────────┘      │
└──────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. **Client → API**: JSON → Request Schema (validation)
2. **Schema → Service**: Request Schema → Entity Data
3. **Service → Schema**: Entity → Response Schema
4. **API → Client**: Response Schema → JSON (serialization)

## Directory Structure Rules

### Organization Pattern

Schemas MUST mirror the routes directory structure exactly:

```
app/domains/{domain}/
├── routes/              # API routes
│   ├── {entity}/
│   │   ├── create.py
│   │   ├── find_all.py
│   │   ├── find_by_id.py
│   │   └── update/
│   │       └── variables.py
│   └── {workflow}/
│       └── publish.py
│
└── schemas/             # API schemas (DTOs)
    ├── {entity}/        # ← SAME structure as routes
    │   ├── create.py
    │   ├── find_all.py
    │   ├── find_by_id.py
    │   └── update/
    │       └── variables.py
    └── {workflow}/
        └── publish.py
```

**Rules:**
- ✅ **DO**: Mirror routes directory structure 1:1
- ✅ **DO**: Use same file names as route files
- ✅ **DO**: Group related operations in subdirectories
- ❌ **DON'T**: Create generic schema files
- ❌ **DON'T**: Deviate from route structure

**Why This Pattern?**
- **Clarity**: Easy to find schemas for any route
- **Maintainability**: Changes to routes reflect in schemas
- **AI-Friendly**: Tools like Cursor can easily navigate
- **Scalability**: Grows naturally with routes
- **Documentation**: Self-documenting structure

### Example Structure

```
schemas/
├── __init__.py                    # Export all schemas
├── prompt/                        # Prompt entity operations
│   ├── __init__.py
│   ├── create.py                  # POST /prompts/
│   ├── find_all.py                # GET /prompts/
│   ├── find_by_id.py              # GET /prompts/{id}
│   ├── find_by_team.py            # GET /prompts/team/{team_id}
│   ├── find_history_by_prompt_id.py   # GET /prompts/{id}/history
│   └── find_versions_by_prompt_id.py  # GET /prompts/{id}/versions
│
├── prompt_version/                # Prompt version operations
│   ├── __init__.py
│   ├── create.py                  # POST /versions/
│   ├── create_iteration.py        # POST /versions/{id}/iteration
│   ├── find_by_id.py              # GET /versions/{id}
│   └── update/                    # Nested update operations
│       ├── __init__.py
│       ├── variables.py           # PATCH /versions/{id}/variables
│       ├── prompt.py              # PATCH /versions/{id}/prompt
│       └── llm_configuration.py   # PATCH /versions/{id}/llm-config
│
└── publish/                       # Workflow operations
    ├── __init__.py
    └── publish.py                 # POST /versions/{id}/publish
```

## Naming Conventions

### Schema Class Names

**Pattern**: `{Operation}{Entity}Schema{Type}`

| Component | Rule | Example |
|-----------|------|---------|
| **Operation** | PascalCase verb | `Create`, `FindAll`, `FindById`, `Update` |
| **Entity** | PascalCase noun | `Prompt`, `PromptVersion`, `TestCase` |
| **Schema** | Literal word | `Schema` |
| **Type** | Request/Response/Item | `Request`, `Response`, `Item` |

### Schema Types

#### 1. Request Schemas (`*SchemaRequest`)

For incoming HTTP request bodies.

```python
class CreatePromptSchemaRequest(BaseModel):
    """Request schema for creating a new prompt."""
    name: str = Field(..., description="Prompt name")
    description: str = Field(..., description="Prompt description")
```

**Examples:**
- `CreatePromptSchemaRequest`
- `UpdateVariablesPromptVersionSchemaRequest`
- `PublishPromptVersionSchemaRequest`

#### 2. Response Schemas (`*SchemaResponse`)

For outgoing HTTP response bodies.

```python
class CreatePromptSchemaResponse(BaseModel):
    """Response schema after creating a prompt."""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Prompt name")
    description: str = Field(..., description="Prompt description")
    
    model_config = ConfigDict(from_attributes=True)
```

**Examples:**
- `CreatePromptSchemaResponse`
- `FindByIdPromptSchemaResponse`
- `PublishPromptVersionSchemaResponse`

#### 3. Item Schemas (`*SchemaItem`)

For individual items in paginated list responses.

```python
class FindAllPromptSchemaItem(BaseModel):
    """Prompt item in find all prompts list response."""
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Prompt name")
    description: str = Field(description="Prompt description")
    
    model_config = ConfigDict(from_attributes=True)
```

**Examples:**
- `FindAllPromptSchemaItem`
- `FindByTeamPromptSchemaItem`
- `FindHistoryByPromptIdPromptSchemaItem`

### File Naming Rules

| File Type | Pattern | Example |
|-----------|---------|---------|
| **Create** | `create.py` | `create.py` |
| **Find All** | `find_all.py` | `find_all.py` |
| **Find by ID** | `find_by_id.py` | `find_by_id.py` |
| **Find by Relation** | `find_by_{relation}.py` | `find_by_team.py` |
| **Find Nested** | `find_{nested}_by_{parent}_id.py` | `find_history_by_prompt_id.py` |
| **Update Full** | `update.py` | `update.py` |
| **Update Partial** | `{field}.py` (in update/) | `update/variables.py` |
| **Delete** | `delete.py` | `delete.py` |
| **Custom Operation** | `{operation}.py` | `publish.py`, `clone.py` |

## Implementation Rules

### Module Docstring

**MUST** include:
1. Brief description of the operation
2. Reference to corresponding route file

```python
"""[Entity] [operation] API schemas.

This module contains request and response schemas for the [operation] route.
Corresponds to: routes/{entity}/{operation}.py
"""
```

**Examples:**

```python
"""Prompt creation API schemas.

This module contains request and response schemas for the create route.
Corresponds to: routes/prompt/create.py
"""
```

```python
"""Update prompt version variables schemas.

This module contains request and response schemas for updating variables.
Corresponds to: routes/prompt_version/update/variables.py
"""
```

### Class Structure

**Order:**
1. **Module docstring** (with route reference)
2. **Imports** (standard lib → third-party → domain)
3. **Request schema** (if applicable)
4. **Item schema** (if list operation)
5. **Response schema**

### Request Schema Pattern

```python
class {Operation}{Entity}SchemaRequest(BaseModel):
    """Request schema for {operation} {entity}.
    
    [Optional: Additional context about the operation].
    
    Attributes:
        field1: Description of field1.
        field2: Description of field2.
    """
    
    field1: str = Field(..., description="Field description", min_length=1)
    field2: int = Field(..., description="Field description", ge=0)
```

**Key Points:**
- Use `Field(...)` for required fields with description
- Use `Field(default, description="...")` for optional fields
- Add validation constraints: `min_length`, `max_length`, `ge`, `le`, `gt`, `lt`
- **NO** `model_config` in request schemas (not converting from entities)

### Response Schema Pattern

```python
class {Operation}{Entity}SchemaResponse(BaseModel):
    """Response schema for {operation} {entity}.
    
    [Optional: What this response represents].
    
    Attributes:
        field1: Description of field1.
        field2: Description of field2.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    field1: str = Field(description="Field description")
    field2: int = Field(description="Field description")
```

**Key Points:**
- **ALWAYS** include `model_config = ConfigDict(from_attributes=True)`
- Place `model_config` immediately after docstring
- Use `Field(description="...")` for all fields
- Can include `...` for required or defaults for optional
- Converts from domain entities using `model_validate(entity)`

### Item Schema Pattern (for Lists)

```python
class {Operation}{Entity}SchemaItem(BaseModel):
    """[Entity] item in {operation} list response.
    
    Attributes:
        field1: Description of field1.
        field2: Description of field2.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    field1: str = Field(description="Field description")
    field2: int = Field(description="Field description")
```

**Key Points:**
- Used for individual items in paginated responses
- Include `model_config` for entity conversion
- Typically includes subset of entity fields
- Used with `PaginationSchemaResponse[ItemType]`

### Paginated Response Pattern

```python
from app.shared.schemas import PaginationSchemaData, PaginationSchemaResponse


class FindAllPromptSchemaItem(BaseModel):
    """Prompt item in find all prompts list response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Prompt name")


class FindAllPromptSchemaResponse(PaginationSchemaResponse[FindAllPromptSchemaItem]):
    """Paginated response for all prompts list.
    
    Attributes:
        data: List of prompts.
        pagination: Pagination metadata.
    """
    
    data: list[FindAllPromptSchemaItem] = Field(description="List of prompts")
    pagination: PaginationSchemaData = Field(description="Pagination metadata")
```

**Key Points:**
- Inherit from `PaginationSchemaResponse[ItemType]`
- Define `Item` schema first
- Use generic type parameter for type safety
- Include both `data` and `pagination` fields

## Documentation Templates

### Template 1: Create Operation

```python
"""[Entity] creation API schemas.

This module contains request and response schemas for the create route.
Corresponds to: routes/{entity}/create.py
"""

from pydantic import BaseModel, ConfigDict, Field


class Create{Entity}SchemaRequest(BaseModel):
    """Request schema for creating a new {entity}.
    
    Attributes:
        name: Name of the {entity}.
        description: Description of the {entity}.
    """
    
    name: str = Field(..., description="{Entity} name", min_length=1)
    description: str = Field(..., description="{Entity} description", min_length=1)


class Create{Entity}SchemaResponse(BaseModel):
    """Response schema after creating a {entity}.
    
    Attributes:
        id: Unique identifier of the created {entity}.
        name: Name of the {entity}.
        description: Description of the {entity}.
        created_at: Creation timestamp.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="{Entity} name")
    description: str = Field(..., description="{Entity} description")
    created_at: datetime = Field(..., description="Creation timestamp")
```

### Template 2: Find All (Paginated)

```python
"""[Entity] find all schemas.

This module contains schemas for listing all {entities} with pagination.
Corresponds to: routes/{entity}/find_all.py
"""

from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import PaginationSchemaData, PaginationSchemaResponse


class FindAll{Entity}SchemaItem(BaseModel):
    """{Entity} item in find all {entities} list response.
    
    Attributes:
        id: Unique identifier.
        name: {Entity} name.
        description: {Entity} description.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier (ULID)")
    name: str = Field(description="{Entity} name")
    description: str = Field(description="{Entity} description")


class FindAll{Entity}SchemaResponse(PaginationSchemaResponse[FindAll{Entity}SchemaItem]):
    """Paginated response for all {entities} list.
    
    Attributes:
        data: List of {entities}.
        pagination: Pagination metadata.
    """
    
    data: list[FindAll{Entity}SchemaItem] = Field(description="List of {entities}")
    pagination: PaginationSchemaData = Field(description="Pagination data")
```

### Template 3: Find by ID

```python
"""[Entity] find by ID schema.

This module contains the response schema for finding a {entity} by ID.
Corresponds to: routes/{entity}/find_by_id.py
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FindById{Entity}SchemaResponse(BaseModel):
    """{Entity} find by ID schema response.
    
    Attributes:
        id: Unique identifier.
        name: {Entity} name.
        description: {Entity} description.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="{Entity} name")
    description: str = Field(..., description="{Entity} description")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
```

### Template 4: Update Operation

```python
"""Update {entity} {field} schemas.

This module contains request and response schemas for updating {field}.
Corresponds to: routes/{entity}/update/{field}.py
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Update{Field}{Entity}SchemaRequest(BaseModel):
    """Request schema for updating {field} in a {entity}.
    
    Attributes:
        {field}: New {field} value.
    """
    
    {field}: dict[str, Any] = Field(
        default_factory=dict,
        description="{Field} to update"
    )


class Update{Field}{Entity}SchemaResponse(BaseModel):
    """Response schema for updating {field} in a {entity}.
    
    Returns the complete updated {entity} entity.
    
    Attributes:
        id: Unique identifier.
        name: {Entity} name.
        {field}: Updated {field}.
        updated_at: Last update timestamp.
        updated_by: User who last updated.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier")
    name: str = Field(description="{Entity} name")
    {field}: dict[str, Any] = Field(
        default_factory=dict,
        description="Updated {field}"
    )
    updated_at: datetime = Field(description="Last update timestamp")
    updated_by: str = Field(description="Last updater user ID")
```

### Template 5: Custom Operation (Workflow)

```python
"""[Operation] {entity} schemas.

This module contains request and response schemas for {operation} operation.
Corresponds to: routes/{workflow}/{operation}.py
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.domains.{domain}.domain.enums import {EnumType}


class {Operation}{Entity}SchemaRequest(BaseModel):
    """Request schema for {operation} a {entity}.
    
    Attributes:
        param1: Description of param1.
        param2: Description of param2.
    """
    
    param1: {EnumType} = Field(description="Parameter 1 description")
    param2: str = Field(description="Parameter 2 description")


class {Operation}{Entity}SchemaResponse(BaseModel):
    """Response schema for {operation} a {entity}.
    
    Attributes:
        message: Success message.
        result_id: ID of the result.
        field1: Description of field1.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    message: str = Field(description="Success message")
    result_id: str = Field(description="ID of the result")
    field1: str = Field(description="Field description")
    created_at: datetime = Field(description="Creation timestamp")
```

## Package Structure

### Schema Package `__init__.py`

```python
"""[Domain] schemas package."""

from .{entity} import (
    Create{Entity}SchemaRequest,
    Create{Entity}SchemaResponse,
    FindAll{Entity}SchemaItem,
    FindAll{Entity}SchemaResponse,
    FindById{Entity}SchemaResponse,
)
from .{other_entity} import (
    Create{OtherEntity}SchemaRequest,
    Create{OtherEntity}SchemaResponse,
)


__all__ = [
    # ===============================
    # {Entity}
    # ===============================
    "Create{Entity}SchemaRequest",
    "Create{Entity}SchemaResponse",
    "FindAll{Entity}SchemaItem",
    "FindAll{Entity}SchemaResponse",
    "FindById{Entity}SchemaResponse",
    
    # ===============================
    # {OtherEntity}
    # ===============================
    "Create{OtherEntity}SchemaRequest",
    "Create{OtherEntity}SchemaResponse",
]
```

**Rules:**
- Group by entity with section comments
- Export all schemas in `__all__`
- Order: Request, Response, Item
- Use descriptive section headers

### Entity Package `__init__.py`

```python
"""[Entity] schemas package."""

from .create import Create{Entity}SchemaRequest, Create{Entity}SchemaResponse
from .find_all import FindAll{Entity}SchemaItem, FindAll{Entity}SchemaResponse
from .find_by_id import FindById{Entity}SchemaResponse
from .update import Update{Entity}SchemaRequest, Update{Entity}SchemaResponse


__all__ = [
    # Create
    "Create{Entity}SchemaRequest",
    "Create{Entity}SchemaResponse",
    
    # Find All
    "FindAll{Entity}SchemaItem",
    "FindAll{Entity}SchemaResponse",
    
    # Find by ID
    "FindById{Entity}SchemaResponse",
    
    # Update
    "Update{Entity}SchemaRequest",
    "Update{Entity}SchemaResponse",
]
```

## Usage in Routes

### Example: Create Route

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
    
    Args:
        request: Prompt creation data (validated by schema).
        current_user: Authenticated user identifier.
        service: Prompt service.
        
    Returns:
        CreatePromptSchemaResponse: Created prompt response.
    """
    # Convert request schema to domain entity
    prompt_data = PromptData.model_validate(request)
    
    # Call service (business logic)
    prompt = await service.create(prompt_data, current_user)
    
    # Convert entity to response schema
    return CreatePromptSchemaResponse.model_validate(prompt)
```

**Data Flow:**
1. **HTTP JSON** → `CreatePromptSchemaRequest` (Pydantic validation)
2. `CreatePromptSchemaRequest` → `PromptData` (domain entity)
3. Service returns `Prompt` (domain entity with ID)
4. `Prompt` → `CreatePromptSchemaResponse` (response schema)
5. **`CreatePromptSchemaResponse`** → HTTP JSON (serialization)

## Field Types and Validation

### Common Field Types

```python
from datetime import datetime
from typing import Any

from pydantic import Field


# String fields
name: str = Field(..., description="Name", min_length=1, max_length=100)
email: str = Field(..., description="Email", pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
description: str | None = Field(None, description="Optional description")

# Integer fields
count: int = Field(..., description="Count", ge=0, le=100)
page: int = Field(1, description="Page number", ge=1)

# Float fields
ratio: float = Field(..., description="Ratio", ge=0.0, le=1.0)

# Boolean fields
is_active: bool = Field(True, description="Active status")

# Datetime fields
created_at: datetime = Field(..., description="Creation timestamp")

# Dict/JSON fields
variables: dict[str, Any] = Field(
    default_factory=dict,
    description="Variables configuration"
)

# List fields
tags: list[str] = Field(default_factory=list, description="Tags")

# Enum fields
from app.domains.xxx.domain.enums import StatusType
status: StatusType = Field(..., description="Status type")

# ULID/UUID fields (in responses)
id: str = Field(..., description="Unique identifier (ULID)")
# OR
from ulid import ULID
id: str | ULID = Field(..., description="Unique identifier")
```

### Validation Constraints

| Constraint | Type | Example |
|------------|------|---------|
| `min_length` | str | `Field(min_length=1)` |
| `max_length` | str | `Field(max_length=100)` |
| `pattern` | str | `Field(pattern=r"^\d{3}-\d{4}$")` |
| `ge` | int/float | `Field(ge=0)` ≥ 0 |
| `gt` | int/float | `Field(gt=0)` > 0 |
| `le` | int/float | `Field(le=100)` ≤ 100 |
| `lt` | int/float | `Field(lt=100)` < 100 |
| `multiple_of` | int/float | `Field(multiple_of=5)` |

### Required vs Optional Fields

```python
# Required field (no default)
name: str = Field(..., description="Name")

# Optional field with None default
description: str | None = Field(None, description="Description")

# Optional field with value default
page: int = Field(1, description="Page number")

# Optional field with factory default (for mutable types)
variables: dict[str, Any] = Field(
    default_factory=dict,
    description="Variables"
)
```

## Best Practices

### ✅ DO

1. **Mirror route structure exactly**
   ```python
   # routes/prompt/create.py → schemas/prompt/create.py ✅
   ```

2. **Reference corresponding route in docstring**
   ```python
   """Prompt creation API schemas.
   
   Corresponds to: routes/prompt/create.py
   """
   ```

3. **Use specific schema names**
   ```python
   class CreatePromptSchemaRequest(BaseModel):  # ✅ Specific
   ```

4. **Include model_config in response schemas**
   ```python
   class CreatePromptSchemaResponse(BaseModel):
       model_config = ConfigDict(from_attributes=True)  # ✅
   ```

5. **Add field descriptions**
   ```python
   name: str = Field(..., description="Prompt name")  # ✅
   ```

6. **Use validation constraints**
   ```python
   name: str = Field(..., min_length=1, max_length=100)  # ✅
   ```

7. **Use type hints for all fields**
   ```python
   variables: dict[str, Any] = Field(...)  # ✅
   ```

8. **Use Pydantic field validators for complex validation**
   ```python
   @field_validator("email")
   @classmethod
   def validate_email(cls, v: str) -> str:  # ✅
       if "@" not in v:
           raise ValueError("Invalid email")
       return v.lower()
   ```

9. **Use default_factory for mutable defaults**
   ```python
   variables: dict[str, Any] = Field(default_factory=dict)  # ✅
   ```

10. **Document all attributes in docstring**
    ```python
    """Request schema.
    
    Attributes:
        name: Name of the entity.
        description: Description of the entity.
    """
    ```

### ❌ DON'T

1. **Don't create generic schema files**
   ```python
   # schemas/generic.py with multiple unrelated schemas ❌
   ```

2. **Don't deviate from route structure**
   ```python
   # routes/prompt/create.py → schemas/crud/create_prompt.py ❌
   ```

3. **Don't use generic names**
   ```python
   class Request(BaseModel):  # ❌ Too generic
   class PromptRequest(BaseModel):  # ❌ Missing operation
   ```

4. **Don't forget model_config in response schemas**
   ```python
   class CreatePromptSchemaResponse(BaseModel):
       # ❌ Missing model_config
       id: str
   ```

5. **Don't forget field descriptions**
   ```python
   name: str = Field(...)  # ❌ No description
   ```

6. **Don't use mutable defaults directly**
   ```python
   variables: dict[str, Any] = Field({})  # ❌ Mutable default
   variables: dict[str, Any] = Field(default_factory=dict)  # ✅
   ```

7. **Don't include business logic**
   ```python
   class CreatePromptSchemaRequest(BaseModel):
       def save_to_database(self):  # ❌ Business logic in schema
           pass
   ```

8. **Don't use ORM models in schemas**
   ```python
   from app.domains.xxx.models import PromptModel  # ❌
   
   class Response(BaseModel):
       prompt: PromptModel  # ❌ Use domain entities
   ```

9. **Don't skip docstrings**
   ```python
   class CreatePromptSchemaRequest(BaseModel):  # ❌ No docstring
       name: str
   ```

10. **Don't mix HTTP concerns**
    ```python
    class Response(BaseModel):
        status_code: int  # ❌ HTTP concern
        headers: dict  # ❌ HTTP concern
    ```

## Schema Type Patterns

### Pattern 1: Simple Create

```python
"""[Entity] creation schemas."""

from pydantic import BaseModel, ConfigDict, Field


class Create{Entity}SchemaRequest(BaseModel):
    """Request for creating {entity}."""
    
    name: str = Field(..., description="Name", min_length=1)
    description: str = Field(..., description="Description")


class Create{Entity}SchemaResponse(BaseModel):
    """Response after creating {entity}."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Name")
    description: str = Field(description="Description")
```

### Pattern 2: Paginated List

```python
"""[Entity] find all schemas."""

from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import PaginationSchemaData, PaginationSchemaResponse


class FindAll{Entity}SchemaItem(BaseModel):
    """Item in {entity} list."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Name")


class FindAll{Entity}SchemaResponse(PaginationSchemaResponse[FindAll{Entity}SchemaItem]):
    """Paginated {entity} list response."""
    
    data: list[FindAll{Entity}SchemaItem] = Field(description="List of {entities}")
    pagination: PaginationSchemaData = Field(description="Pagination metadata")
```

### Pattern 3: Find by ID (Detail)

```python
"""[Entity] find by ID schema."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FindById{Entity}SchemaResponse(BaseModel):
    """Detailed {entity} response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Name")
    description: str = Field(description="Description")
    metadata: dict[str, Any] | None = Field(None, description="Metadata")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
```

### Pattern 4: Partial Update

```python
"""Update {entity} {field} schemas."""

from pydantic import BaseModel, ConfigDict, Field


class Update{Field}{Entity}SchemaRequest(BaseModel):
    """Request for updating {field}."""
    
    {field}: str = Field(..., description="{Field} value")


class Update{Field}{Entity}SchemaResponse(BaseModel):
    """Response after updating {field}."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier")
    {field}: str = Field(description="Updated {field}")
    updated_at: datetime = Field(description="Update timestamp")
    updated_by: str = Field(description="Updater user ID")
```

### Pattern 5: No Request Body (Query Params Only)

```python
"""[Entity] find by team schema."""

from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import PaginationSchemaData, PaginationSchemaResponse


# No request schema needed (query params handled by FastAPI)


class FindByTeam{Entity}SchemaItem(BaseModel):
    """Item in team {entity} list."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier")
    name: str = Field(description="Name")


class FindByTeam{Entity}SchemaResponse(
    PaginationSchemaResponse[FindByTeam{Entity}SchemaItem]
):
    """Paginated team {entity} list response."""
    
    data: list[FindByTeam{Entity}SchemaItem] = Field(description="List of {entities}")
    pagination: PaginationSchemaData = Field(description="Pagination metadata")
```

### Pattern 6: Workflow Operation

```python
"""Publish {entity} schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domains.{domain}.domain.enums import VersionType


class Publish{Entity}SchemaRequest(BaseModel):
    """Request for publishing {entity}."""
    
    version_type: VersionType = Field(
        description="Version increment type (MAJOR, MINOR, PATCH)"
    )


class Publish{Entity}SchemaResponse(BaseModel):
    """Response after publishing {entity}."""
    
    model_config = ConfigDict(from_attributes=True)
    
    message: str = Field(description="Success message")
    history_id: str = Field(description="Created history ID")
    version: str = Field(description="New semantic version")
    created_at: datetime = Field(description="Creation timestamp")
```

## Real-World Examples

### Example 1: Create Prompt

**File**: `schemas/prompt/create.py`

```python
"""Prompt creation API schemas.

This module contains request and response schemas for the create route.
Corresponds to: routes/prompt/create.py
"""

from pydantic import BaseModel, ConfigDict, Field
from ulid import ULID


class CreatePromptSchemaRequest(BaseModel):
    """Request schema for creating a new prompt.
    
    Attributes:
        name: Name of the prompt.
        description: Description of what the prompt does.
    """
    
    name: str = Field(..., description="Prompt name", min_length=1)
    description: str = Field(..., description="Prompt description", min_length=1)


class CreatePromptSchemaResponse(BaseModel):
    """Response schema after creating a prompt.
    
    Attributes:
        id: Unique identifier of the created prompt.
        name: Name of the prompt.
        description: Description of the prompt.
        current_version: Current semantic version.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str | ULID = Field(..., description="Unique identifier")
    name: str = Field(..., description="Prompt name")
    description: str = Field(..., description="Prompt description")
    current_version: str = Field(..., description="Current version")
```

### Example 2: Find All Prompts (Paginated)

**File**: `schemas/prompt/find_all.py`

```python
"""Prompt find all schemas.

This module contains schemas for listing all prompts with pagination.
Corresponds to: routes/prompt/find_all.py
"""

from pydantic import BaseModel, ConfigDict, Field

from app.shared.schemas import PaginationSchemaData, PaginationSchemaResponse


class FindAllPromptSchemaItem(BaseModel):
    """Prompt item in find all prompts list response.
    
    Attributes:
        id: Unique identifier.
        name: Prompt name.
        description: Prompt description.
        current_version: Current semantic version.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier (ULID)")
    name: str = Field(description="Prompt name")
    description: str = Field(description="Prompt description")
    current_version: str = Field(description="Current version")


class FindAllPromptSchemaResponse(PaginationSchemaResponse[FindAllPromptSchemaItem]):
    """Paginated response for all prompts list.
    
    Attributes:
        data: List of all prompts.
        pagination: Pagination metadata.
    """
    
    data: list[FindAllPromptSchemaItem] = Field(description="List of prompts")
    pagination: PaginationSchemaData = Field(description="Pagination data")
```

### Example 3: Update Variables

**File**: `schemas/prompt_version/update/variables.py`

```python
"""Update prompt version variables schemas.

This module contains request and response schemas for updating variables.
Corresponds to: routes/prompt_version/update/variables.py
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class UpdateVariablesPromptVersionSchemaRequest(BaseModel):
    """Request schema for updating variables in a prompt version.
    
    Attributes:
        variables: Variables dictionary to update.
    """
    
    variables: dict[str, Any] = Field(
        default_factory=dict,
        description="Variables to update"
    )


class UpdateVariablesPromptVersionSchemaResponse(BaseModel):
    """Response schema for updating variables in a prompt version.
    
    Returns the complete updated prompt version entity.
    
    Attributes:
        id: Unique identifier of the prompt version.
        prompt_id: ID of the parent prompt.
        variables: Updated variables configuration.
        updated_at: Last update timestamp.
        updated_by: User who last updated the version.
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    id: str = Field(description="Unique identifier")
    prompt_id: str = Field(description="Parent prompt ID")
    variables: dict[str, Any] = Field(
        default_factory=dict,
        description="Prompt variables"
    )
    updated_at: datetime = Field(description="Last update timestamp")
    updated_by: str = Field(description="Last updater user ID")
```

## Required Elements Checklist

- [ ] Module docstring describing the operation
- [ ] Module docstring references corresponding route file
- [ ] Imports follow standard order (stdlib → third-party → domain)
- [ ] Request schema (if operation has body)
- [ ] Response schema (always)
- [ ] Item schema (if paginated list)
- [ ] Class docstrings with purpose
- [ ] Attributes section in docstrings
- [ ] All fields have descriptions
- [ ] Validation constraints on fields
- [ ] `model_config = ConfigDict(from_attributes=True)` in response schemas
- [ ] Type hints for all fields
- [ ] File name matches route file name
- [ ] File location mirrors route structure
- [ ] Schema exported in package `__init__.py`

## Common Mistakes

### Mistake 1: Wrong Structure

```python
# ❌ BAD - Doesn't mirror routes
schemas/
└── prompt_schemas.py  # All prompt schemas in one file

# ✅ GOOD - Mirrors routes
schemas/
└── prompt/
    ├── create.py
    ├── find_all.py
    └── find_by_id.py
```

### Mistake 2: Missing model_config

```python
# ❌ BAD - Missing model_config
class CreatePromptSchemaResponse(BaseModel):
    id: str
    name: str

# ✅ GOOD - Includes model_config
class CreatePromptSchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    name: str
```

### Mistake 3: Mutable Default

```python
# ❌ BAD - Mutable default
variables: dict[str, Any] = Field({})

# ✅ GOOD - Factory default
variables: dict[str, Any] = Field(default_factory=dict)
```

### Mistake 4: Missing Descriptions

```python
# ❌ BAD - No descriptions
name: str = Field(...)
description: str = Field(...)

# ✅ GOOD - With descriptions
name: str = Field(..., description="Prompt name")
description: str = Field(..., description="Prompt description")
```

## References

- **Services.md**: For service layer that uses schemas
- **Entities.md**: For domain entities that schemas convert to/from
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **DTO Pattern**: Martin Fowler - Patterns of Enterprise Application Architecture
- **Clean Architecture**: Robert C. Martin (Uncle Bob)

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-31 | Initial comprehensive schemas documentation |

