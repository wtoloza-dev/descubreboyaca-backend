# Import Patterns

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Import Patterns** | `All Layers` | `DDD` `Clean Architecture` `Code Organization` |

## Definition

Import patterns define how modules reference each other within the codebase. Proper import patterns maintain layer boundaries, reduce coupling, and improve code maintainability.

## Core Rules

### Absolute vs Relative Imports

| Import Type | Usage | Example |
|-------------|-------|---------|
| **Absolute** | Cross-layer imports, shared utilities | `from app.shared.domain.entities import Audit` |
| **Relative** | Same-layer imports (max 2-3 levels) | `from .value_objects import PromptData` |

### Layer Boundaries

**✅ Allowed:**
- Relative imports **within the same architectural layer**
- Maximum **2-3 levels** of relative navigation
- Imports from outer layers (domain → shared)

**❌ Forbidden:**
- Relative imports **across different layers**
- More than 3 levels of relative navigation (`../../../`)
- Imports from inner layers (repositories → domain is OK, but not vice versa for implementation details)

## Relative Import Rules

### Maximum Depth: 2-3 Levels

```python
# ✅ CORRECT - 1 level (same directory)
from .prompt_version import PromptVersion
from .value_objects import PromptData

# ✅ CORRECT - 2 levels (parent directory)
from ..entities import Audit
from ..exceptions import PromptNotFoundError

# ✅ CORRECT - 3 levels (grandparent directory - maximum)
from ...shared.domain.entities import BaseEntity

# ❌ INCORRECT - 4+ levels (too deep)
from ....app.shared.domain.entities import Audit
```

### Same Layer Requirements

Relative imports are **only allowed** when both modules belong to the **same architectural layer**:

| Layer | Example Path | Can Use Relative Imports With |
|-------|--------------|-------------------------------|
| Domain (Entities) | `app/domains/prompt/domain/entities/` | Other files in `domain/entities/` subdirectory |
| Domain (Enums) | `app/domains/prompt/domain/enums/` | Other files in `domain/enums/` subdirectory |
| Domain (Exceptions) | `app/domains/prompt/domain/exceptions/` | Other files in `domain/exceptions/` subdirectory |
| Domain (Interfaces) | `app/domains/prompt/domain/interfaces/` | Other files in `domain/interfaces/` subdirectory |
| Domain (Value Objects) | `app/domains/prompt/domain/value_objects/` | Other files in `domain/value_objects/` subdirectory |
| Repositories | `app/domains/prompt/repositories/` | Other files in `repositories/` subdirectory |
| Routes | `app/domains/prompt/routes/` | Other files in `routes/` subdirectory |
| Schemas | `app/domains/prompt/schemas/` | Other files in `schemas/` subdirectory |

## Pattern Examples

### Domain Layer (Entities)

```python
"""Prompt domain entities following DDD principles."""

# File: app/domains/prompt/domain/entities/prompt.py

# ✅ CORRECT - Absolute import from shared layer
from app.shared.domain.entities import Audit
from pydantic import BaseModel, Field, ConfigDict

# ✅ CORRECT - Relative import within same domain/entities layer (1 level)
from .prompt_version import PromptVersionData

# ✅ CORRECT - Relative import from domain/value_objects (2 levels up, then down)
from ..value_objects import SemanticVersion


class Prompt(PromptData, Audit):
    """Prompt entity with identity and audit fields."""
    pass
```

### Domain Layer (Value Objects)

```python
"""Prompt value objects."""

# File: app/domains/prompt/domain/value_objects/semantic_version.py

from pydantic import BaseModel, Field, ConfigDict


class SemanticVersion(BaseModel):
    """Semantic version value object."""
    
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)
    
    major: int = Field(description="Major version")
    minor: int = Field(description="Minor version")
    patch: int = Field(description="Patch version")
```

### Domain Layer (Cross-Subdirectory within Domain)

```python
"""Prompt entity using value objects."""

# File: app/domains/prompt/domain/entities/prompt.py

from pydantic import BaseModel, Field, ConfigDict

# ✅ CORRECT - Relative import from sibling entity file (same domain/entities)
from .prompt_version import PromptVersion

# ✅ CORRECT - Relative import from domain/value_objects (2 levels)
from ..value_objects.semantic_version import SemanticVersion

# ✅ CORRECT - Relative import from domain/enums (2 levels)
from ..enums.access_level import AccessLevel

# ✅ CORRECT - Absolute import from shared layer
from app.shared.domain.entities import Audit
```

### Repository Layer

```python
"""Prompt repository implementation."""

# ✅ CORRECT - Absolute imports from domain layer (cross-layer)
from app.domains.prompt.entities import Prompt
from app.clients.sql.ports.sql import SQLPort

# ✅ CORRECT - Relative import within repository layer (2 levels)
from ..common.sql import BasePromptRepository


class PromptRepository(BasePromptRepository):
    """SQLite implementation of prompt repository."""
    pass
```

### Routes Layer

```python
"""Prompt API routes."""

from fastapi import APIRouter, Depends

# ✅ CORRECT - Absolute imports from other layers
from app.domains.prompt.schemas import PromptCreateSchema, PromptResponseSchema
from app.domains.prompt.services import PromptService

# ✅ CORRECT - Relative import within routes layer (1 level)
from .dependencies import get_prompt_service


router = APIRouter()


@router.post("/prompts")
async def create_prompt(
    data: PromptCreateSchema,
    service: PromptService = Depends(get_prompt_service),
) -> PromptResponseSchema:
    """Create new prompt."""
    return await service.create_prompt(data)
```

### Schemas Layer

```python
"""Prompt request/response schemas."""

from pydantic import BaseModel, Field

# ✅ CORRECT - Relative import within schemas layer (1 level)
from .common import BaseResponseSchema


class PromptResponseSchema(BaseResponseSchema):
    """Prompt response schema."""
    
    prompt_id: str = Field(description="Prompt identifier")
    name: str = Field(description="Prompt name")
```

## Common Patterns by Location

### Within Domain Subdirectory

```python
# File: app/domains/prompt/domain/entities/prompt.py

# ✅ Same subdirectory (domain/entities) - Use relative (1 level)
from .prompt_version import PromptVersion

# ✅ Same domain layer, different subdirectory (domain/value_objects) - Use relative (2 levels)
from ..value_objects.semantic_version import SemanticVersion

# ✅ Same domain layer, different subdirectory (domain/enums) - Use relative (2 levels)
from ..enums.access_level import AccessLevel

# ✅ Cross-layer (shared) - Use absolute
from app.shared.domain.entities import Audit
```

```python
# File: app/domains/prompt/domain/exceptions/prompt.py

# ✅ Same subdirectory (domain/exceptions) - Use relative (1 level)
from .base import PromptBaseException

# ✅ Same domain layer (domain/enums) - Use relative (2 levels)
from ..enums.access_level import AccessLevel

# ✅ Cross-layer (shared exceptions) - Use absolute
from app.shared.domain.exceptions import DomainException
```

### Within Repository Subdirectory

```python
# File: app/domains/prompt/repositories/prompt/sqlite.py

# ✅ Same layer (repositories), 2 levels up to common - Use relative
from ..common.sql import BasePromptRepository

# ✅ Same layer (repositories), sibling directory - Use relative  
from ...prompt_history.common.sql import PromptHistoryQueries

# ✅ Cross-layer (domain entities) - Use absolute
from app.domains.prompt.entities import Prompt
from app.clients.sql.ports.sql import SQLPort
```

### Within Routes Subdirectory

```python
# File: app/domains/prompt/routes/prompt_routes.py

# ✅ Same layer (routes), dependencies file - Use relative
from .dependencies import get_prompt_service
from ..dependencies.auth import get_current_user

# ✅ Cross-layer (schemas, services) - Use absolute
from app.domains.prompt.schemas import PromptCreateSchema
from app.domains.prompt.services import PromptService
```

## Anti-Patterns

### ❌ Incorrect: Relative Imports Across Layers

```python
# File: app/domains/prompt/routes/prompt_routes.py

# ❌ WRONG - Routes trying to use relative import to schemas (different layer)
from ..schemas.prompt_schema import PromptResponseSchema

# ✅ CORRECT - Use absolute import
from app.domains.prompt.schemas import PromptResponseSchema
```

```python
# File: app/domains/prompt/domain/entities/prompt.py

# ❌ WRONG - Domain trying to use relative import to repositories (different layer)
from ....repositories.prompt.common.sql import PromptRepository

# ✅ CORRECT - Use absolute import (though domain shouldn't import repositories)
from app.domains.prompt.repositories import PromptRepository
```

### ❌ Incorrect: Too Many Levels

```python
# File: app/domains/prompt/repositories/prompt/common/sql.py

# ❌ WRONG - 4+ levels up
from ......shared.domain.entities import Audit

# ✅ CORRECT - Use absolute import
from app.shared.domain.entities import Audit
```

### ❌ Incorrect: Relative for Shared Utilities

```python
# File: app/domains/prompt/domain/entities/prompt.py

# ❌ WRONG - Relative import to shared layer (4+ levels)
from .....shared.domain.entities import Audit

# ✅ CORRECT - Absolute import for shared utilities
from app.shared.domain.entities import Audit
```

## Decision Tree

```
Need to import a module?
│
├─ Is it in the SAME architectural layer?
│  │
│  ├─ YES → Is it within 2-3 directory levels?
│  │  │
│  │  ├─ YES → ✅ Use RELATIVE import
│  │  │         from .module import Class
│  │  │         from ..sibling import Class
│  │  │
│  │  └─ NO → ✅ Use ABSOLUTE import
│  │            from app.domains.prompt.module import Class
│  │
│  └─ NO → ✅ Use ABSOLUTE import
│           from app.shared.domain.entities import Audit
```

## Layer Definition Reference

| Layer Type | Path Pattern | Examples |
|------------|--------------|----------|
| **Domain/Entities** | `app/domains/{domain}/domain/entities/` | Business entities |
| **Domain/Value Objects** | `app/domains/{domain}/domain/value_objects/` | Value objects |
| **Domain/Enums** | `app/domains/{domain}/domain/enums/` | Domain-specific enumerations |
| **Domain/Exceptions** | `app/domains/{domain}/domain/exceptions/` | Domain-specific exceptions |
| **Domain/Interfaces** | `app/domains/{domain}/domain/interfaces/` | Repository interfaces, ports |
| **Models** | `app/domains/{domain}/models/` | Database models (SQLAlchemy) |
| **Repositories** | `app/domains/{domain}/repositories/` | Data access implementations |
| **Routes** | `app/domains/{domain}/routes/` | API endpoints |
| **Schemas** | `app/domains/{domain}/schemas/` | Request/response models |
| **Services** | `app/domains/{domain}/services/` | Application services |
| **Dependencies** | `app/domains/{domain}/dependencies/` | Dependency injection |
| **Shared** | `app/shared/` | Cross-domain utilities |
| **Clients** | `app/clients/` | External service clients |

### Domain Layer Structure

The `domain/` folder contains the core business logic organized in subdirectories:

```
app/domains/{domain}/domain/
├── entities/          ← Domain entities (Audit + Data)
├── value_objects/     ← Value objects (immutable data)
├── enums/            ← Domain-specific enumerations
├── exceptions/       ← Domain-specific exceptions
└── interfaces/       ← Repository interfaces (ports)
```

**Important:** All subdirectories within `domain/` are considered part of the **same layer** for relative import purposes (max 2-3 levels).

## Checklist

- [ ] Relative imports only within same architectural layer
- [ ] Maximum 2-3 levels of relative navigation (`..` or `...`)
- [ ] Absolute imports for cross-layer dependencies
- [ ] Absolute imports for shared utilities (`app.shared.*`)
- [ ] Absolute imports for client libraries (`app.clients.*`)
- [ ] No circular dependencies between layers
- [ ] Clear separation of concerns maintained

## Benefits

### Relative Imports (Same Layer)
- ✅ Easier refactoring within a layer
- ✅ Clear indication of module proximity
- ✅ Less verbose for nearby modules

### Absolute Imports (Cross-Layer)
- ✅ Clear architectural boundaries
- ✅ Easy to understand dependencies
- ✅ Better IDE/tooling support
- ✅ Prevents circular dependencies

