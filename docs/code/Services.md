# Domain Services

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Domain Services** | `Application/Domain Layer` | `DDD` `Clean Architecture` `Hexagonal Architecture` `SOLID` |

## Definition

Domain Services encapsulate and orchestrate business logic that doesn't naturally fit within a single entity or value object. They coordinate between multiple repositories, enforce business rules, manage transactions, and handle domain workflows. Services act as the use case layer in Clean Architecture, keeping business logic independent of infrastructure concerns.

**Key Characteristics:**
- **Business Logic Orchestration**: Coordinate complex domain operations
- **Repository Coordination**: Manage multiple repository interactions
- **Transaction Management**: Control atomic operations across aggregates
- **Domain-Centric**: Work only with domain entities, not ORM models
- **Infrastructure-Agnostic**: No knowledge of HTTP, databases, or external systems
- **Stateless**: No instance state between method calls
- **Dependency Injection**: Receive dependencies through constructor

## Service Layer Pattern

```
┌────────────────────────────────────────────────────────────┐
│                   Presentation Layer                       │
│                  (Routes/Controllers)                      │
│                 - HTTP Request/Response                    │
│                 - Data validation (Schemas)                │
└───────────────────────┬────────────────────────────────────┘
                        │ calls
┌───────────────────────┴────────────────────────────────────┐
│                   Application Layer                        │
│                    (Domain Services)                       │
│   ┌─────────────────────────────────────────────────┐      │
│   │           PromptService                         │      │
│   │  - Orchestrates business logic                  │      │
│   │  - Coordinates repositories                     │      │
│   │  - Manages transactions                         │      │
│   │  - Raises domain exceptions                     │      │
│   └──────────┬─────────────────┬────────────────────┘      │
└──────────────┼─────────────────┼───────────────────────────┘
               │                 │ uses
┌──────────────┴─────────────────┴───────────────────────────┐
│                     Domain Layer                           │
│  ┌─────────────────────┐    ┌────────────────────────┐     │
│  │ Repository Interface│    │ Domain Entities        │     │
│  │    (Protocol)       │    │ (Entities, VOs)        │     │
│  └──────────┬──────────┘    └────────────────────────┘     │
└─────────────┼──────────────────────────────────────────────┘
              │ implements
┌─────────────┴──────────────────────────────────────────────┐
│                Infrastructure Layer                        │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │ MySQL Repository     │  │ SQLite Repository    │        │
│  │  (Implementation)    │  │  (Implementation)    │        │
│  └──────────────────────┘  └──────────────────────┘        │
└────────────────────────────────────────────────────────────┘
```

**Responsibilities by Layer:**

| Layer | Responsibilities | Examples |
|-------|-----------------|----------|
| **Presentation** | HTTP, validation, serialization | Routes, schemas, dependencies |
| **Application (Service)** | Business logic, orchestration | Services, use cases |
| **Domain** | Core business rules, entities | Entities, value objects, interfaces |
| **Infrastructure** | External systems, persistence | Repository implementations, clients |

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Directory | `services/` | `app/domains/prompt/services/` |
| Filename | `{entity}_snake_case.py` | `prompt.py`, `prompt_version.py` |
| Class Name | `{Entity}Service` | `PromptService`, `PromptVersionService` |
| Workflow Services | `{workflow}.py` | `publish.py` (PublishService) |

## Implementation Rules

### Basic Structure

```python
"""[Entity] service for business logic orchestration.

This module contains the service layer for [Entity] domain operations.
Services handle business logic, coordinate between repositories, and manage
domain exceptions.
"""

from app.domains.xxx.domain.entities import Entity, EntityData
from app.domains.xxx.domain.exceptions import (
    EntityNotFoundException,
    EntityAlreadyExistsException,
)
from app.domains.xxx.domain.interfaces import EntityRepositoryInterface


class EntityService:
    """[Entity] service for business logic orchestration.
    
    [Brief description of service responsibilities and key business rules].
    
    Attributes:
        repository: Entity repository interface.
        other_repository: Optional related repository interface.
    """
    
    def __init__(
        self,
        repository: EntityRepositoryInterface,
        other_repository: OtherRepositoryInterface | None = None,
    ) -> None:
        """Initialize service with repository dependencies.
        
        Args:
            repository: Entity repository implementation.
            other_repository: Optional related repository implementation.
        """
        self.repository = repository
        self.other_repository = other_repository
    
    async def get_by_id(self, entity_id: str) -> Entity:
        """Get entity by ID.
        
        Args:
            entity_id: Entity identifier.
            
        Returns:
            Entity: Entity domain entity.
            
        Raises:
            EntityNotFoundException: If entity not found.
        """
        entity = await self.repository.get_by_id(entity_id)
        if not entity:
            raise EntityNotFoundException(entity_id=entity_id)
        return entity
    
    async def create(self, entity_data: EntityData, created_by: str) -> Entity:
        """Create a new entity.
        
        Args:
            entity_data: Entity business data.
            created_by: User identifier for audit trail.
            
        Returns:
            Entity: Created entity.
            
        Raises:
            EntityAlreadyExistsException: If entity already exists.
        """
        # Business validation here
        return await self.repository.create(
            entity=entity_data,
            created_by=created_by,
        )
```

### Class Structure Order

1. **Module docstring** (describing service purpose)
2. **Imports** (standard lib → third-party → domain → repositories)
3. **Class docstring** (describing responsibilities)
4. **`__init__` method** (dependency injection)
5. **Query methods** (find, get, list, count)
6. **Command methods** (create, update, delete)
7. **Business logic methods** (domain-specific operations)
8. **Transaction orchestration methods** (complex workflows)

### Constructor Pattern

**Always use dependency injection:**

```python
def __init__(
    self,
    repository: EntityRepositoryInterface,
    related_repository: RelatedRepositoryInterface | None = None,
) -> None:
    """Initialize service with repository dependencies.
    
    Args:
        repository: Entity repository implementation.
        related_repository: Optional related repository.
    """
    self.repository = repository
    self.related_repository = related_repository
```

**Key Points:**
- Accept **interfaces**, not implementations
- Store repositories as instance attributes
- Use type hints for all parameters
- Make optional dependencies explicit with `| None`
- Document all dependencies

### Method Patterns

#### 1. Query Methods (Read Operations)

**Pattern: Get by ID with Exception**

```python
async def get_by_id(self, entity_id: str) -> Entity:
    """Get entity by ID.
    
    Args:
        entity_id: Entity identifier.
        
    Returns:
        Entity: Entity domain entity.
        
    Raises:
        EntityNotFoundException: If entity not found.
    """
    entity = await self.repository.get_by_id(entity_id)
    if not entity:
        raise EntityNotFoundException(entity_id=entity_id)
    return entity
```

**Pattern: Find with Pagination**

```python
async def find(
    self,
    filters: dict[str, Any] | None = None,
    offset: int = 0,
    limit: int = 10,
) -> tuple[list[Entity], int]:
    """Find entities with optional filters and pagination.
    
    Args:
        filters: Filter criteria dictionary (e.g., {"name": "Test"}).
        offset: Number of records to skip.
        limit: Maximum records to return.
        
    Returns:
        Tuple[list[Entity], int]: Tuple of (entities list, total count).
    """
    search_filters = filters or {}
    entities = await self.repository.find(
        filters=search_filters,
        offset=offset,
        limit=limit,
    )
    total = await self.repository.count(filters=search_filters)
    return entities, total
```

**Pattern: Find by Related Entity**

```python
async def find_by_owner(
    self,
    owner_type: OwnerType,
    owner_id: str,
    offset: int = 0,
    limit: int = 10,
) -> tuple[list[Entity], int]:
    """Find entities by owner.
    
    Args:
        owner_type: Type of owner (USER, TEAM, APP).
        owner_id: Owner identifier.
        offset: Number of records to skip.
        limit: Maximum records to return.
        
    Returns:
        Tuple[list[Entity], int]: Tuple of (entities list, total count).
    """
    # Query through relationship
    ownerships = await self.ownership_repository.find_by_owner(
        owner_type, owner_id
    )
    
    if not ownerships:
        return [], 0
    
    # Get entities by IDs
    entity_ids = [ownership.entity_id for ownership in ownerships]
    entities = []
    for entity_id in entity_ids[offset : offset + limit]:
        entity = await self.repository.get_by_id(entity_id)
        if entity:
            entities.append(entity)
    
    return entities, len(entity_ids)
```

#### 2. Command Methods (Write Operations)

**Pattern: Create Entity**

```python
async def create(
    self,
    entity_data: EntityData,
    created_by: str,
) -> Entity:
    """Create a new entity.
    
    Args:
        entity_data: Entity business data.
        created_by: User identifier for audit trail.
        
    Returns:
        Entity: Created entity.
    """
    return await self.repository.create(
        entity=entity_data,
        created_by=created_by,
    )
```

**Pattern: Update Entity**

```python
async def update(
    self,
    entity_id: str,
    entity_data: EntityData,
    updated_by: str,
) -> Entity:
    """Update an existing entity.
    
    Args:
        entity_id: Entity identifier.
        entity_data: Updated entity data.
        updated_by: User identifier for audit trail.
        
    Returns:
        Entity: Updated entity.
        
    Raises:
        EntityNotFoundException: If entity not found.
    """
    # Verify entity exists
    await self.get_by_id(entity_id)
    
    # Update entity
    updated_entity = await self.repository.update(
        id=entity_id,
        entity=entity_data,
        updated_by=updated_by,
    )
    
    if not updated_entity:
        raise EntityNotFoundException(entity_id=entity_id)
    
    return updated_entity
```

**Pattern: Soft Delete**

```python
async def delete(self, entity_id: str, deleted_by: str) -> None:
    """Delete entity (soft delete).
    
    Marks the entity as deleted without removing it from the database.
    
    Args:
        entity_id: Entity identifier to delete.
        deleted_by: User identifier for audit trail.
        
    Raises:
        EntityNotFoundException: If entity not found.
    """
    deleted = await self.repository.delete(entity_id, deleted_by)
    if not deleted:
        raise EntityNotFoundException(entity_id=entity_id)
```

**Pattern: Hard Delete (Admin Only)**

```python
async def hard_delete(self, entity_id: str) -> None:
    """Permanently delete entity from storage.
    
    Warning: This operation cannot be undone and is intended for
    administrative purposes only (e.g., test cleanup, data purging).
    
    Args:
        entity_id: Entity identifier to permanently delete.
        
    Raises:
        EntityNotFoundException: If entity not found.
    """
    deleted = await self.repository.hard_delete(entity_id)
    if not deleted:
        raise EntityNotFoundException(entity_id=entity_id)
```

#### 3. Complex Business Logic

**Pattern: Create with Related Entities (Transaction)**

```python
async def create_with_ownership(
    self,
    entity_data: EntityData,
    created_by: str,
) -> Entity:
    """Create entity with automatic ownership.
    
    Creates entity and establishes primary ownership for the creator.
    This is an atomic operation - both succeed or both fail.
    
    Args:
        entity_data: Entity business data.
        created_by: User identifier.
        
    Returns:
        Entity: Created entity with ownership.
    """
    # Create entity (no commit)
    entity = await self.repository.create(
        entity=entity_data,
        created_by=created_by,
        commit=False,
    )
    
    # Create primary ownership (no commit)
    ownership_data = OwnershipData(
        entity_id=entity.id,
        owner_type=OwnerType.USER,
        owner_id=created_by,
        access_level=AccessLevel.OWNER,
        is_primary=True,
    )
    await self.ownership_repository.create(
        ownership=ownership_data,
        created_by=created_by,
        commit=False,
    )
    
    # Commit everything atomically
    await self.repository.commit()
    
    return entity
```

**Pattern: Multi-Step Workflow**

```python
async def publish_version(
    self,
    version_id: str,
    version_type: VersionType,
    current_user: str,
) -> History:
    """Publish development version to production.
    
    This orchestrates a complex workflow:
    1. Validate development version exists
    2. Validate parent entity exists
    3. Check for version conflicts
    4. Compute next semantic version
    5. Update entity with production data
    6. Create history record
    7. Commit atomically
    
    Args:
        version_id: Development version identifier.
        version_type: Version increment type (MAJOR, MINOR, PATCH).
        current_user: User performing the publish.
        
    Returns:
        History: Created history record.
        
    Raises:
        VersionNotFoundException: If version not found.
        EntityNotFoundException: If entity not found.
        VersionConflictException: If version conflict detected.
    """
    # 1. Get and validate development version
    dev_version = await self.version_repository.get_by_id(version_id)
    if not dev_version:
        raise VersionNotFoundException(version_id=version_id)
    
    # 2. Get and validate parent entity
    entity = await self.repository.get_by_id(dev_version.entity_id)
    if not entity:
        raise EntityNotFoundException(entity_id=dev_version.entity_id)
    
    # 3. Validate version conflict
    if dev_version.source_version != entity.current_version:
        raise VersionConflictException(
            dev_version.source_version,
            entity.current_version,
        )
    
    # 4. Compute next version
    next_version = self._compute_next_version(
        entity.current_version,
        version_type,
    )
    
    # 5. Update entity (no commit)
    entity_data = EntityData(
        name=entity.name,
        description=dev_version.description,
        current_version=next_version,
        # ... other fields from dev_version
    )
    await self.repository.update(
        id=entity.id,
        entity=entity_data,
        updated_by=current_user,
        commit=False,
    )
    
    # 6. Create history record (no commit)
    history_data = HistoryData(
        entity_id=entity.id,
        version=next_version,
        description=dev_version.description,
        # ... other fields
    )
    history = await self.history_repository.create(
        entity=history_data,
        created_by=current_user,
        commit=False,
    )
    
    # 7. Commit everything atomically
    await self.repository.commit()
    
    return history

def _compute_next_version(
    self,
    current_version: str,
    version_type: VersionType,
) -> str:
    """Compute next semantic version.
    
    Private helper method for version calculation.
    
    Args:
        current_version: Current semantic version.
        version_type: Type of version increment.
        
    Returns:
        str: Next semantic version.
    """
    semver = SemanticVersion.from_string(current_version)
    
    if version_type == VersionType.MAJOR:
        return semver.increment_major().to_string()
    elif version_type == VersionType.MINOR:
        return semver.increment_minor().to_string()
    elif version_type == VersionType.PATCH:
        return semver.increment_patch().to_string()
    else:
        raise InvalidVersionTypeException(version_type)
```

#### 4. Partial Update Methods

**Pattern: Update Specific Fields**

```python
async def update_description(
    self,
    entity_id: str,
    description: str,
    updated_by: str,
) -> Entity:
    """Update entity description only.
    
    Args:
        entity_id: Entity identifier.
        description: New description.
        updated_by: User identifier.
        
    Returns:
        Entity: Updated entity.
        
    Raises:
        EntityNotFoundException: If entity not found.
    """
    # Get existing entity
    existing = await self.get_by_id(entity_id)
    
    # Create updated entity data
    entity_data = EntityData.model_validate(existing)
    entity_data.description = description
    
    # Update
    updated = await self.repository.update(
        id=entity_id,
        entity=entity_data,
        updated_by=updated_by,
    )
    
    if not updated:
        raise EntityNotFoundException(entity_id=entity_id)
    
    return updated
```

### Error Handling Strategy

**Services MUST raise domain exceptions:**

```python
# ✅ CORRECT - Service raises domain exception
async def get_by_id(self, entity_id: str) -> Entity:
    entity = await self.repository.get_by_id(entity_id)
    if not entity:
        raise EntityNotFoundException(entity_id=entity_id)  # ✅
    return entity

# ❌ INCORRECT - Service returns None (repositories do this)
async def get_by_id(self, entity_id: str) -> Entity | None:
    return await self.repository.get_by_id(entity_id)  # ❌
```

**Exception Handling Responsibilities:**

| Layer | Responsibility | Example |
|-------|---------------|---------|
| **Repository** | Return `None`, `[]`, or `False` | `get_by_id() -> Entity \| None` |
| **Service** | Raise domain exceptions | `raise EntityNotFoundException()` |
| **Route** | Catch and return HTTP responses | Handled by exception handlers |

### Transaction Management

**Pattern 1: Single Operation (Auto-Commit)**

```python
async def create(self, entity_data: EntityData, created_by: str) -> Entity:
    """Create entity with automatic commit."""
    return await self.repository.create(
        entity=entity_data,
        created_by=created_by,
        commit=True,  # Default, can be omitted
    )
```

**Pattern 2: Multiple Operations (Manual Transaction)**

```python
async def create_with_related(
    self,
    entity_data: EntityData,
    related_data: RelatedData,
    created_by: str,
) -> Entity:
    """Create entity with related data atomically."""
    try:
        # All operations with commit=False
        entity = await self.repository.create(
            entity=entity_data,
            created_by=created_by,
            commit=False,
        )
        
        related_data.entity_id = entity.id
        await self.related_repository.create(
            entity=related_data,
            created_by=created_by,
            commit=False,
        )
        
        # Commit everything at once
        await self.repository.commit()
        await self.related_repository.commit()
        
        return entity
        
    except Exception:
        # Rollback on any error
        await self.repository.rollback()
        await self.related_repository.rollback()
        raise
```

**Pattern 3: Conditional Commit**

```python
async def update_with_validation(
    self,
    entity_id: str,
    entity_data: EntityData,
    updated_by: str,
) -> Entity:
    """Update with business validation."""
    # Start without committing
    entity = await self.repository.update(
        id=entity_id,
        entity=entity_data,
        updated_by=updated_by,
        commit=False,
    )
    
    if not entity:
        await self.repository.rollback()
        raise EntityNotFoundException(entity_id=entity_id)
    
    # Business validation
    if not self._validate_business_rules(entity):
        await self.repository.rollback()
        raise ValidationException("Business rules not met")
    
    # All good, commit
    await self.repository.commit()
    return entity
```

## Docstring Requirements

### Module Docstring

```python
"""[Entity] service for business logic orchestration.

This module contains the service layer for [Entity] domain operations.
Services handle business logic, coordinate between repositories, and manage
domain exceptions.
"""
```

### Class Docstring

```python
class EntityService:
    """[Entity] service for business logic orchestration.
    
    [Brief description of service's main responsibilities].
    [Mention any important business rules it enforces].
    
    Attributes:
        repository: Entity repository interface.
        other_repository: Related repository interface.
    """
```

### Method Docstring (Google Style)

```python
async def create(
    self,
    entity_data: EntityData,
    created_by: str,
) -> Entity:
    """Create a new entity.
    
    [Optional: Additional details about the operation].
    [Optional: Business rules enforced].
    
    Args:
        entity_data: Entity business data.
        created_by: User identifier for audit trail.
        
    Returns:
        Entity: Created entity with identity and audit fields.
        
    Raises:
        EntityAlreadyExistsException: If entity already exists.
        ValidationException: If business rules not met.
    """
```

## Documentation Templates

### Basic CRUD Service

```python
"""[Entity] service for business logic orchestration.

This module contains the service layer for [Entity] domain operations.
Services handle business logic, coordinate between repositories, and manage
domain exceptions.
"""

from typing import Any

from app.domains.xxx.domain.entities import Entity, EntityData
from app.domains.xxx.domain.exceptions import EntityNotFoundException
from app.domains.xxx.domain.interfaces import EntityRepositoryInterface


class EntityService:
    """[Entity] service for business logic orchestration.
    
    Handles CRUD operations and business logic for [entity] entities.
    
    Attributes:
        repository: Entity repository interface.
    """
    
    def __init__(self, repository: EntityRepositoryInterface) -> None:
        """Initialize service with repository dependency.
        
        Args:
            repository: Entity repository implementation.
        """
        self.repository = repository
    
    async def find(
        self,
        filters: dict[str, Any] | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> tuple[list[Entity], int]:
        """Find entities with optional filters and pagination.
        
        Args:
            filters: Filter criteria dictionary.
            offset: Number of records to skip.
            limit: Maximum records to return.
            
        Returns:
            Tuple[list[Entity], int]: Tuple of (entities list, total count).
        """
        search_filters = filters or {}
        entities = await self.repository.find(
            filters=search_filters,
            offset=offset,
            limit=limit,
        )
        total = await self.repository.count(filters=search_filters)
        return entities, total
    
    async def get_by_id(self, entity_id: str) -> Entity:
        """Get entity by ID.
        
        Args:
            entity_id: Entity identifier.
            
        Returns:
            Entity: Entity domain entity.
            
        Raises:
            EntityNotFoundException: If entity not found.
        """
        entity = await self.repository.get_by_id(entity_id)
        if not entity:
            raise EntityNotFoundException(entity_id=entity_id)
        return entity
    
    async def create(
        self,
        entity_data: EntityData,
        created_by: str,
    ) -> Entity:
        """Create a new entity.
        
        Args:
            entity_data: Entity business data.
            created_by: User identifier for audit trail.
            
        Returns:
            Entity: Created entity.
        """
        return await self.repository.create(
            entity=entity_data,
            created_by=created_by,
        )
    
    async def update(
        self,
        entity_id: str,
        entity_data: EntityData,
        updated_by: str,
    ) -> Entity:
        """Update an existing entity.
        
        Args:
            entity_id: Entity identifier.
            entity_data: Updated entity data.
            updated_by: User identifier for audit trail.
            
        Returns:
            Entity: Updated entity.
            
        Raises:
            EntityNotFoundException: If entity not found.
        """
        await self.get_by_id(entity_id)
        
        updated = await self.repository.update(
            id=entity_id,
            entity=entity_data,
            updated_by=updated_by,
        )
        
        if not updated:
            raise EntityNotFoundException(entity_id=entity_id)
        
        return updated
    
    async def delete(self, entity_id: str, deleted_by: str) -> None:
        """Delete entity (soft delete).
        
        Args:
            entity_id: Entity identifier to delete.
            deleted_by: User identifier for audit trail.
            
        Raises:
            EntityNotFoundException: If entity not found.
        """
        deleted = await self.repository.delete(entity_id, deleted_by)
        if not deleted:
            raise EntityNotFoundException(entity_id=entity_id)
    
    async def hard_delete(self, entity_id: str) -> None:
        """Permanently delete entity from storage.
        
        Warning: This operation cannot be undone and is intended for
        administrative purposes only.
        
        Args:
            entity_id: Entity identifier to permanently delete.
            
        Raises:
            EntityNotFoundException: If entity not found.
        """
        deleted = await self.repository.hard_delete(entity_id)
        if not deleted:
            raise EntityNotFoundException(entity_id=entity_id)
```

### Service with Multiple Repositories

```python
"""Prompt service for business logic orchestration.

This module contains the service layer for Prompt domain operations.
Services handle business logic, coordinate between repositories, and manage
domain exceptions.
"""

from typing import Any

from app.domains.prompt.domain.entities import (
    Prompt,
    PromptData,
    PromptOwnershipData,
)
from app.domains.prompt.domain.enums import AccessLevel, OwnerType
from app.domains.prompt.domain.exceptions import PromptNotFoundException
from app.domains.prompt.domain.interfaces import (
    PromptOwnershipRepositoryInterface,
    PromptRepositoryInterface,
)


class PromptService:
    """Prompt service for business logic orchestration.
    
    Coordinates prompt operations and ownership management. Enforces business
    rules like creating primary ownership when prompts are created.
    
    Attributes:
        repository: Prompt repository interface.
        ownership_repository: Prompt ownership repository interface.
    """
    
    def __init__(
        self,
        repository: PromptRepositoryInterface,
        ownership_repository: PromptOwnershipRepositoryInterface,
    ) -> None:
        """Initialize service with repositories.
        
        Args:
            repository: Prompt repository implementation.
            ownership_repository: Prompt ownership repository implementation.
        """
        self.repository = repository
        self.ownership_repository = ownership_repository
    
    async def get_by_id(self, prompt_id: str) -> Prompt:
        """Get prompt by ID.
        
        Args:
            prompt_id: Prompt identifier.
            
        Returns:
            Prompt: Prompt entity.
            
        Raises:
            PromptNotFoundException: If prompt not found.
        """
        prompt = await self.repository.get_by_id(prompt_id)
        if not prompt:
            raise PromptNotFoundException(prompt_id=prompt_id)
        return prompt
    
    async def create(
        self,
        prompt_data: PromptData,
        created_by: str,
    ) -> Prompt:
        """Create prompt with primary ownership.
        
        This method creates a prompt and automatically establishes primary
        ownership for the creator. Both operations are atomic.
        
        Args:
            prompt_data: Prompt data.
            created_by: User identifier.
            
        Returns:
            Prompt: Created prompt entity.
        """
        # Create prompt (no commit)
        prompt = await self.repository.create(
            prompt=prompt_data,
            created_by=created_by,
            commit=False,
        )
        
        # Create primary ownership (no commit)
        ownership_data = PromptOwnershipData(
            prompt_id=prompt.id,
            owner_type=OwnerType.USER,
            owner_id=created_by,
            access_level=AccessLevel.OWNER,
            is_primary=True,
        )
        await self.ownership_repository.create(
            ownership=ownership_data,
            created_by=created_by,
            commit=False,
        )
        
        # Commit everything atomically
        await self.repository.commit()
        
        return prompt
```

### Workflow Service

```python
"""Publish service for promoting versions to production.

This service orchestrates the publish workflow, which includes:
1. Validating the development version and entity
2. Checking for version conflicts
3. Computing the next semantic version
4. Creating a history record
5. Updating the entity with production data
"""

from app.domains.xxx.domain.entities import Entity, History, HistoryData, Version
from app.domains.xxx.domain.enums import VersionType
from app.domains.xxx.domain.exceptions import (
    EntityNotFoundException,
    InvalidVersionTypeException,
    VersionConflictException,
    VersionNotFoundException,
)
from app.domains.xxx.domain.interfaces import (
    EntityRepositoryInterface,
    HistoryRepositoryInterface,
    VersionRepositoryInterface,
)
from app.domains.xxx.domain.value_objects import SemanticVersion


class PublishService:
    """Service for publishing versions to production.
    
    This service orchestrates the process of promoting a development version
    to production by validating, versioning, and persisting changes across
    multiple entities.
    """
    
    def __init__(
        self,
        entity_repository: EntityRepositoryInterface,
        version_repository: VersionRepositoryInterface,
        history_repository: HistoryRepositoryInterface,
    ):
        """Initialize the publish service with repository dependencies.
        
        Args:
            entity_repository: Repository for entity operations.
            version_repository: Repository for version operations.
            history_repository: Repository for history operations.
        """
        self.entity_repository = entity_repository
        self.version_repository = version_repository
        self.history_repository = history_repository
    
    async def publish_version(
        self,
        version_id: str,
        version_type: str,
        current_user: str,
    ) -> History:
        """Publish a development version to production (atomic transaction).
        
        This method orchestrates the entire publish workflow:
        1. Retrieves and validates the development version
        2. Retrieves and validates the parent entity
        3. Checks for version conflicts
        4. Computes the next semantic version
        5. Updates the entity with production data (no commit)
        6. Creates a history record (no commit)
        7. Commits everything atomically
        
        Args:
            version_id: ID of the development version to publish.
            version_type: Type of version increment (MAJOR, MINOR, PATCH).
            current_user: Current user ID for authorization and tracking.
            
        Returns:
            History: The created history entity.
            
        Raises:
            VersionNotFoundException: If the dev version doesn't exist.
            EntityNotFoundException: If the entity doesn't exist.
            VersionConflictException: If source_version doesn't match.
            InvalidVersionTypeException: If version type is invalid.
        """
        # Implementation here...
```

### Package Structure (`__init__.py`)

```python
"""[Domain] services package."""

from .entity import EntityService
from .related import RelatedService
from .workflow import WorkflowService


__all__ = [
    # Entity services
    "EntityService",
    "RelatedService",
    # Workflow services
    "WorkflowService",
]
```

## Best Practices

### ✅ DO

1. **Use dependency injection**
   ```python
   def __init__(
       self,
       repository: EntityRepositoryInterface,  # ✅ Interface, not implementation
   ) -> None:
   ```

2. **Raise domain exceptions**
   ```python
   if not entity:
       raise EntityNotFoundException(entity_id=entity_id)  # ✅
   ```

3. **Work with domain entities**
   ```python
   async def create(self, entity_data: EntityData, ...) -> Entity:  # ✅
   ```

4. **Use async/await**
   ```python
   async def get_by_id(self, entity_id: str) -> Entity:  # ✅
   ```

5. **Document all methods with Google-style docstrings**
   ```python
   async def create(self, entity_data: EntityData, created_by: str) -> Entity:
       """Create a new entity.
       
       Args:
           entity_data: Entity business data.
           created_by: User identifier for audit trail.
           
       Returns:
           Entity: Created entity.
       """
   ```

6. **Handle transactions explicitly**
   ```python
   entity = await self.repository.create(..., commit=False)  # ✅
   await self.related_repository.create(..., commit=False)
   await self.repository.commit()
   ```

7. **Return domain entities, never ORM models**
   ```python
   async def get_by_id(self, entity_id: str) -> Entity:  # ✅ Entity
   ```

8. **Use type hints everywhere**
   ```python
   async def find(...) -> tuple[list[Entity], int]:  # ✅
   ```

9. **Validate in service layer**
   ```python
   # Verify related entity exists
   await self.related_service.get_by_id(entity_data.related_id)  # ✅
   ```

10. **Make services stateless**
    ```python
    class EntityService:
        def __init__(self, repository: EntityRepositoryInterface):
            self.repository = repository  # ✅ Only dependencies
            # ❌ No business state between calls
    ```

### ❌ DON'T

1. **Don't work with ORM models**
   ```python
   async def create(self, model: EntityModel, ...) -> EntityModel:  # ❌
   ```

2. **Don't return None (use exceptions)**
   ```python
   async def get_by_id(self, entity_id: str) -> Entity | None:  # ❌
       return await self.repository.get_by_id(entity_id)
   ```

3. **Don't use synchronous methods**
   ```python
   def get_by_id(self, entity_id: str) -> Entity:  # ❌ Missing async
   ```

4. **Don't accept implementations in constructor**
   ```python
   def __init__(self, repository: MySQLEntityRepository):  # ❌
       # Should accept EntityRepositoryInterface
   ```

5. **Don't mix HTTP concerns**
   ```python
   async def create(self, request: Request, ...) -> Response:  # ❌
       # Services should be HTTP-agnostic
   ```

6. **Don't handle HTTP status codes**
   ```python
   if not entity:
       return {"status": 404, "error": "Not found"}  # ❌
   ```

7. **Don't forget error handling**
   ```python
   async def get_by_id(self, entity_id: str) -> Entity:
       return await self.repository.get_by_id(entity_id)  # ❌ No exception
   ```

8. **Don't skip docstrings**
   ```python
   async def complex_workflow(self, ...):  # ❌ No docstring
   ```

9. **Don't store state between calls**
   ```python
   class EntityService:
       def __init__(self, repository):
           self.repository = repository
           self.current_user = None  # ❌ State between calls
   ```

10. **Don't mix business logic in routes**
    ```python
    # In route:
    prompt = await repository.create(...)  # ❌ Business logic in route
    await ownership_repository.create(...)
    
    # Should be:
    prompt = await service.create(...)  # ✅ Service handles logic
    ```

## Common Patterns

### Pattern 1: Simple CRUD Service

Basic service with standard create, read, update, delete operations.

```python
class EntityService:
    """Basic CRUD service."""
    
    def __init__(self, repository: EntityRepositoryInterface) -> None:
        self.repository = repository
    
    async def find(...) -> tuple[list[Entity], int]: ...
    async def get_by_id(...) -> Entity: ...
    async def create(...) -> Entity: ...
    async def update(...) -> Entity: ...
    async def delete(...) -> None: ...
```

### Pattern 2: Coordinating Service

Service that coordinates multiple repositories.

```python
class PromptService:
    """Service coordinating multiple repositories."""
    
    def __init__(
        self,
        repository: PromptRepositoryInterface,
        ownership_repository: PromptOwnershipRepositoryInterface,
    ) -> None:
        self.repository = repository
        self.ownership_repository = ownership_repository
    
    async def create_with_ownership(...) -> Prompt:
        """Create prompt with ownership atomically."""
        # Coordinate multiple repositories
```

### Pattern 3: Workflow Service

Service for complex multi-step workflows.

```python
class PublishService:
    """Service for complex publish workflow."""
    
    def __init__(
        self,
        entity_repository: EntityRepositoryInterface,
        version_repository: VersionRepositoryInterface,
        history_repository: HistoryRepositoryInterface,
    ) -> None:
        self.entity_repository = entity_repository
        self.version_repository = version_repository
        self.history_repository = history_repository
    
    async def publish_version(...) -> History:
        """Multi-step workflow with validation and transactions."""
        # Complex workflow logic
```

### Pattern 4: Service with Business Validation

Service that validates against other services.

```python
class TestCaseService:
    """Service with cross-entity validation."""
    
    def __init__(
        self,
        repository: TestCaseRepositoryInterface,
        prompt_service: PromptService | None = None,
    ) -> None:
        self.repository = repository
        self.prompt_service = prompt_service
    
    async def create(self, entity_data: TestCaseData, created_by: str) -> TestCase:
        """Create test case with prompt validation."""
        # Validate prompt exists
        if self.prompt_service:
            await self.prompt_service.get_by_id(entity_data.prompt_id)
        
        return await self.repository.create(
            entity=entity_data,
            created_by=created_by,
        )
```

### Pattern 5: Read-Only Service

Service for read-only operations (e.g., history, logs).

```python
class HistoryService:
    """Read-only service for history records."""
    
    def __init__(self, repository: HistoryRepositoryInterface) -> None:
        self.repository = repository
    
    async def list_by_entity(...) -> list[History]: ...
    async def get_by_id(...) -> History: ...
    async def count_by_entity(...) -> int: ...
    
    # No create, update, delete for history (append-only)
```

## Service Testing

### Unit Testing Services

```python
import pytest
from unittest.mock import AsyncMock

from app.domains.prompt.domain.entities import Prompt, PromptData
from app.domains.prompt.domain.exceptions import PromptNotFoundException
from app.domains.prompt.services import PromptService


@pytest.fixture
def mock_repository():
    """Mock repository for testing."""
    return AsyncMock()


@pytest.fixture
def service(mock_repository):
    """Service instance with mock repository."""
    return PromptService(repository=mock_repository)


@pytest.mark.asyncio
async def test_get_by_id_success(service, mock_repository):
    """Test successful get by ID."""
    # Arrange
    prompt_id = "01HQ123ABC"
    expected_prompt = Prompt(
        id=prompt_id,
        name="Test Prompt",
        created_by="user123",
        updated_by="user123",
    )
    mock_repository.get_by_id.return_value = expected_prompt
    
    # Act
    result = await service.get_by_id(prompt_id)
    
    # Assert
    assert result == expected_prompt
    mock_repository.get_by_id.assert_called_once_with(prompt_id)


@pytest.mark.asyncio
async def test_get_by_id_not_found(service, mock_repository):
    """Test get by ID raises exception when not found."""
    # Arrange
    prompt_id = "nonexistent"
    mock_repository.get_by_id.return_value = None
    
    # Act & Assert
    with pytest.raises(PromptNotFoundException) as exc_info:
        await service.get_by_id(prompt_id)
    
    assert exc_info.value.context["prompt_id"] == prompt_id


@pytest.mark.asyncio
async def test_create_success(service, mock_repository):
    """Test successful create."""
    # Arrange
    prompt_data = PromptData(
        name="Test Prompt",
        description="Test description",
    )
    created_prompt = Prompt(
        id="01HQ123ABC",
        name=prompt_data.name,
        description=prompt_data.description,
        created_by="user123",
        updated_by="user123",
    )
    mock_repository.create.return_value = created_prompt
    
    # Act
    result = await service.create(prompt_data, "user123")
    
    # Assert
    assert result.id == "01HQ123ABC"
    assert result.name == "Test Prompt"
    mock_repository.create.assert_called_once_with(
        entity=prompt_data,
        created_by="user123",
    )
```

### Integration Testing Services

```python
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.prompt.repositories import MySQLPromptRepository
from app.domains.prompt.services import PromptService


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_and_get_prompt(db_session: AsyncSession):
    """Test create and retrieve prompt (integration test)."""
    # Arrange
    repository = MySQLPromptRepository(session=db_session)
    service = PromptService(repository=repository)
    
    prompt_data = PromptData(
        name="Integration Test Prompt",
        description="Test description",
    )
    
    # Act - Create
    created_prompt = await service.create(prompt_data, "user123")
    
    # Act - Retrieve
    retrieved_prompt = await service.get_by_id(created_prompt.id)
    
    # Assert
    assert retrieved_prompt.id == created_prompt.id
    assert retrieved_prompt.name == "Integration Test Prompt"
    assert retrieved_prompt.created_by == "user123"
```

## When to Create Services

### ✅ Create Service When:

- Need to coordinate multiple repositories
- Complex business logic doesn't fit in entities
- Workflows require multiple steps/validation
- Need transaction management across aggregates
- Following Clean Architecture/DDD patterns
- Need to enforce business rules

### ❌ Don't Create Service When:

- Simple CRUD with single repository (use repository directly in routes)
- No business logic (just pass-through to repository)
- Pure calculation (use value object methods)
- Infrastructure concern (use infrastructure layer)

## Required Elements Checklist

- [ ] Module docstring describing service purpose
- [ ] Import domain entities (not ORM models)
- [ ] Import domain exceptions
- [ ] Import repository interfaces (not implementations)
- [ ] Class inherits from nothing (plain class)
- [ ] Class docstring with responsibilities
- [ ] `__init__` uses dependency injection
- [ ] All methods are `async`
- [ ] All methods have complete docstrings (Google style)
- [ ] All methods have type hints
- [ ] Query methods return domain entities
- [ ] Services raise domain exceptions (not return None)
- [ ] Transaction management for multi-step operations
- [ ] No HTTP concerns (Request, Response, status codes)
- [ ] No ORM models in signatures
- [ ] Service is stateless (no business state between calls)
- [ ] Exported in `__init__.py`

## Architecture Principles

### SOLID Principles

**Single Responsibility Principle**
- Each service has one clear responsibility
- Separate services for distinct workflows

**Open/Closed Principle**
- Services depend on interfaces, not implementations
- Easy to extend with new implementations

**Liskov Substitution Principle**
- Repository implementations are interchangeable
- Mock repositories for testing

**Interface Segregation Principle**
- Services only depend on interfaces they use
- No fat interfaces

**Dependency Inversion Principle**
- Services depend on abstractions (interfaces)
- Infrastructure depends on domain (not vice versa)

### Clean Architecture

```
Outer → Inner Dependencies:
Routes → Services → Domain (Entities, VOs, Interfaces)
         ↓
    Infrastructure (Repositories, Clients)
```

**Rules:**
- Services (Application Layer) orchestrate domain logic
- Services depend on domain interfaces, not infrastructure
- Infrastructure implements domain interfaces
- Domain has no dependencies on outer layers

### Domain-Driven Design

**Services in DDD:**
- **Application Services** (this document): Orchestrate use cases
- **Domain Services**: Business logic that doesn't fit in entities
- **Infrastructure Services**: External system integration

**When to Use Application Services:**
- Coordinating multiple aggregates
- Transaction boundaries
- Use case orchestration
- Business workflow management

## References

- **Repository_Interfaces.md**: For repository contracts
- **Entities.md**: For domain entities
- **Value_Objects.md**: For value objects
- **Exceptions.md**: For domain exceptions
- **Clean Architecture**: Robert C. Martin (Uncle Bob)
- **Domain-Driven Design**: Eric Evans
- **Implementing DDD**: Vaughn Vernon
- **Patterns of Enterprise Application Architecture**: Martin Fowler

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-31 | Initial comprehensive services documentation |

