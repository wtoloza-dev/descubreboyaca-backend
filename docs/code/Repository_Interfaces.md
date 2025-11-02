# Domain Interfaces (Repository Interfaces)

## Tags

| Name | Layer | Architecture |
|------|-------|--------------|
| **Repository Interfaces** | `Domain Layer` | `DDD` `Ports & Adapters` `Dependency Inversion` |

## Definition

Repository Interfaces define contracts for data persistence operations in the domain layer. They follow the **Repository Pattern** from DDD and the **Dependency Inversion Principle** from SOLID, allowing the domain to remain independent of infrastructure concerns.

**Key Characteristics:**
- **Infrastructure-Agnostic**: No coupling to specific databases or ORMs
- **Domain-Centric**: Return domain entities, not ORM models
- **Async-First**: All operations use async/await for scalability
- **Protocol-Based**: Use Python's `Protocol` for structural subtyping
- **Transaction-Aware**: Support commit/rollback operations

## Repository Pattern

```
┌─────────────────────────────────────────────────────────┐
│                     Domain Layer                        │
│  ┌──────────────┐         ┌────────────────────────┐    │
│  │   Service    │ ───────→│ Repository Interface   │    │
│  │   (Logic)    │         │      (Protocol)        │    │
│  └──────────────┘         └────────────────────────┘    │
└─────────────────────────────────────┬───────────────────┘
                                      │ implements
┌─────────────────────────────────────┴───────────────────┐
│                Infrastructure Layer                     │
│  ┌──────────────────────┐  ┌──────────────────────┐     │
│  │ MySQL Repository     │  │ SQLite Repository    │     │
│  │  (Implementation)    │  │  (Implementation)    │     │
│  └──────────────────────┘  └──────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

**Benefits:**
- Domain is decoupled from infrastructure
- Easy to swap database implementations
- Testable with mock repositories
- Clear separation of concerns

## File & Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| Directory | `domain/interfaces/` | `app/domains/prompt/domain/interfaces/` |
| Filename | `{entity}_repository.py` | `prompt_repository.py` |
| Interface Name | `{Entity}RepositoryInterface` | `PromptRepositoryInterface` |
| Implementation Directory | `repositories/{entity}/` | `repositories/prompt/` |
| Implementation Name | `{Database}{Entity}Repository` | `MySQLPromptRepository` |

## Implementation Rules

### Basic Structure

```python
"""[Entity] repository interface."""

from typing import Any, Protocol

from ..entities import Entity, EntityData


class EntityRepositoryInterface(Protocol):
    """[Entity] repository interface.
    
    Defines contract for persistence operations on [entity] entities.
    """
    
    async def find(
        self,
        filters: dict[str, Any],
        offset: int = 0,
        limit: int = 10,
    ) -> list[Entity]:
        """Find entities by filters with pagination.
        
        Args:
            filters: Dictionary with filter criteria.
            offset: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            list[Entity]: List of entities matching the filters.
                Empty list if none found.
        """
        ...
    
    async def get_by_id(self, id: str) -> Entity | None:
        """Get an entity by id.
        
        Args:
            id: Unique identifier of the entity.
            
        Returns:
            Entity | None: The entity if found, None otherwise.
        """
        ...
    
    async def create(
        self,
        entity: EntityData,
        created_by: str,
        commit: bool = True,
    ) -> Entity:
        """Create an entity.
        
        Args:
            entity: Business data for the new entity.
            created_by: User identifier for audit trail.
            commit: Whether to commit the transaction. Defaults to True.
            
        Returns:
            Entity: The created entity with identity and audit fields.
        """
        ...
    
    async def update(
        self,
        id: str,
        entity: EntityData,
        updated_by: str,
        commit: bool = True,
    ) -> Entity | None:
        """Update an entity.
        
        Args:
            id: Unique identifier of the entity to update.
            entity: Business data to update.
            updated_by: User identifier for audit trail.
            commit: Whether to commit the transaction. Defaults to True.
            
        Returns:
            Entity | None: The updated entity if found, None otherwise.
        """
        ...
    
    async def delete(
        self,
        id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete an entity (soft delete).
        
        Args:
            id: Unique identifier of the entity to delete.
            deleted_by: User identifier for audit trail.
            commit: Whether to commit the transaction. Defaults to True.
            
        Returns:
            bool: True if the entity was deleted, False if not found.
        """
        ...
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        ...
    
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        ...
```

### Method Structure Order

1. **Query methods** (find, count, get_by_id, etc.)
2. **Command methods** (create, update, delete)
3. **Business-specific methods** (check_access, revoke_access, etc.)
4. **Transaction methods** (commit, rollback) - Always last

### Protocol vs ABC

**Use `Protocol` (Structural Subtyping)** ✅
```python
from typing import Protocol

class EntityRepositoryInterface(Protocol):
    async def get_by_id(self, id: str) -> Entity | None:
        ...
```

**Why Protocol?**
- No explicit inheritance required
- Implementation can be anywhere
- Better for dependency injection
- More Pythonic and flexible
- Duck typing with type checking

**Don't use ABC** ❌
```python
from abc import ABC, abstractmethod

class EntityRepositoryInterface(ABC):  # ❌ Too rigid
    @abstractmethod
    async def get_by_id(self, id: str) -> Entity | None:
        pass
```

### Type Annotations

#### Return Types

**Query Operations:**
- Single entity: `Entity | None` (None if not found)
- Multiple entities: `list[Entity]` (empty list if none found)
- Count operations: `int`
- Boolean checks: `bool`

**Command Operations:**
- Create: `Entity` (always returns created entity)
- Update: `Entity | None` (None if not found)
- Delete: `bool` (True if deleted, False if not found)

**Examples:**
```python
# ✅ CORRECT - Single entity returns None if not found
async def get_by_id(self, id: str) -> Entity | None:
    ...

# ✅ CORRECT - Multiple entities return empty list
async def find(self, filters: dict[str, Any]) -> list[Entity]:
    ...

# ❌ INCORRECT - Don't raise exceptions in interface
async def get_by_id(self, id: str) -> Entity:  # Missing | None
    """Raises: EntityNotFoundException"""  # ❌ Wrong layer
    ...
```

### Parameter Naming Conventions

| Parameter | Type | Convention | Example |
|-----------|------|------------|---------|
| Entity ID | `str` | `id` or `{entity}_id` | `id`, `prompt_id` |
| Business Data | `EntityData` | `entity` or `{entity}` | `entity`, `prompt` |
| User Audit | `str` | `created_by`, `updated_by`, `deleted_by` | `created_by` |
| Filters | `dict[str, Any]` | `filters` | `filters` |
| Pagination | `int` | `offset`, `limit` | `offset=0, limit=10` |
| Ordering | `str \| None` | `order` | `order="desc"` |
| Transaction | `bool` | `commit` | `commit=True` |

### Docstring Requirements

Each method **MUST** have:
1. **Brief description** (one line)
2. **Args section** with all parameters
3. **Returns section** with type and description
4. **Optional**: Raises section (only if exceptional)

**Example:**
```python
async def create(
    self,
    entity: EntityData,
    created_by: str,
    commit: bool = True,
) -> Entity:
    """Create an entity.
    
    Args:
        entity: Business data for the new entity.
        created_by: User identifier for audit trail.
        commit: Whether to commit the transaction. Defaults to True.
        
    Returns:
        Entity: The created entity with identity and audit fields.
    """
    ...
```

## Standard CRUD Methods

### 1. Query Methods

#### find()

Find multiple entities with filters and pagination.

```python
async def find(
    self,
    filters: dict[str, Any],
    offset: int = 0,
    limit: int = 10,
    order: str | None = None,
) -> list[Entity]:
    """Find entities by filters with pagination.
    
    Args:
        filters: Dictionary with filter criteria.
        offset: Number of records to skip.
        limit: Maximum number of records to return.
        order: Ordering direction (asc or desc).
        
    Returns:
        list[Entity]: List of entities matching the filters.
            Empty list if none found.
    """
    ...
```

#### count()

Count entities matching filters.

```python
async def count(self, filters: dict[str, Any]) -> int:
    """Count entities matching the filters.
    
    Args:
        filters: Dictionary with filter criteria.
        
    Returns:
        int: Total number of entities matching the filters.
    """
    ...
```

#### get_by_id()

Get a single entity by ID.

```python
async def get_by_id(self, id: str) -> Entity | None:
    """Get an entity by id.
    
    Args:
        id: Unique identifier of the entity.
        
    Returns:
        Entity | None: The entity if found, None otherwise.
    """
    ...
```

### 2. Command Methods

#### create()

Create a new entity.

```python
async def create(
    self,
    entity: EntityData,
    created_by: str,
    commit: bool = True,
) -> Entity:
    """Create an entity.
    
    Args:
        entity: Business data for the new entity.
        created_by: User identifier for audit trail.
        commit: Whether to commit the transaction. Defaults to True.
        
    Returns:
        Entity: The created entity with identity and audit fields.
    """
    ...
```

#### update()

Update an existing entity.

```python
async def update(
    self,
    id: str,
    entity: EntityData,
    updated_by: str,
    commit: bool = True,
) -> Entity | None:
    """Update an entity.
    
    Args:
        id: Unique identifier of the entity to update.
        entity: Business data to update.
        updated_by: User identifier for audit trail.
        commit: Whether to commit the transaction. Defaults to True.
        
    Returns:
        Entity | None: The updated entity if found, None otherwise.
    """
    ...
```

#### delete()

Soft delete an entity (sets deleted_at).

```python
async def delete(
    self,
    id: str,
    deleted_by: str,
    commit: bool = True,
) -> bool:
    """Delete an entity (soft delete).
    
    Args:
        id: Unique identifier of the entity to delete.
        deleted_by: User identifier for audit trail.
        commit: Whether to commit the transaction. Defaults to True.
        
    Returns:
        bool: True if the entity was deleted, False if not found.
    """
    ...
```

#### hard_delete()

Permanently delete an entity.

```python
async def hard_delete(self, id: str) -> bool:
    """Permanently delete an entity from storage.
    
    Warning: This operation cannot be undone. Use with extreme caution.
    This is intended for administrative purposes only.
    
    Args:
        id: Unique identifier of the entity to permanently delete.
        
    Returns:
        bool: True if the entity was deleted, False if not found.
    """
    ...
```

### 3. Transaction Methods

Always include these last:

```python
async def commit(self) -> None:
    """Commit the current transaction."""
    ...

async def rollback(self) -> None:
    """Rollback the current transaction."""
    ...
```

## Domain-Specific Methods

Beyond CRUD, add business-specific query methods:

### Access Control Example

```python
async def check_access(
    self,
    prompt_id: str,
    owner_type: OwnerType,
    owner_id: str,
    required_level: AccessLevel,
) -> bool:
    """Check if owner has required access level to prompt.
    
    Args:
        prompt_id: Unique identifier of the prompt.
        owner_type: Type of owner entity.
        owner_id: Identifier of the owner.
        required_level: Minimum required access level.
        
    Returns:
        bool: True if owner has required access level or higher, False otherwise.
    """
    ...
```

### Relationship Queries Example

```python
async def find_by_prompt_id(self, prompt_id: str) -> list[PromptOwnership]:
    """Find all ownership records for a specific prompt.
    
    Args:
        prompt_id: Unique identifier of the prompt.
        
    Returns:
        list[PromptOwnership]: All ownership records for the prompt.
            Empty list if no owners found.
    """
    ...

async def find_by_owner(
    self, owner_type: OwnerType, owner_id: str
) -> list[PromptOwnership]:
    """Find all ownership records for a specific owner.
    
    Args:
        owner_type: Type of owner entity.
        owner_id: Identifier of the owner.
        
    Returns:
        list[PromptOwnership]: All ownership records for the owner.
            Empty list if no records found.
    """
    ...
```

## Documentation Template

### Basic Repository Interface

```python
"""[Entity] repository interface."""

from typing import Any, Protocol

from ..entities import Entity, EntityData


class EntityRepositoryInterface(Protocol):
    """[Entity] repository interface.
    
    Defines contract for persistence operations on [entity] entities.
    """
    
    async def find(
        self,
        filters: dict[str, Any],
        offset: int = 0,
        limit: int = 10,
    ) -> list[Entity]:
        """Find entities by filters with pagination.
        
        Args:
            filters: Dictionary with filter criteria.
            offset: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            list[Entity]: List of entities matching the filters.
        """
        ...
    
    async def count(self, filters: dict[str, Any]) -> int:
        """Count entities matching the filters.
        
        Args:
            filters: Dictionary with filter criteria.
            
        Returns:
            int: Total number of entities matching the filters.
        """
        ...
    
    async def get_by_id(self, id: str) -> Entity | None:
        """Get an entity by id.
        
        Args:
            id: Unique identifier of the entity.
            
        Returns:
            Entity | None: The entity if found, None otherwise.
        """
        ...
    
    async def create(
        self,
        entity: EntityData,
        created_by: str,
        commit: bool = True,
    ) -> Entity:
        """Create an entity.
        
        Args:
            entity: Business data for the new entity.
            created_by: User identifier for audit trail.
            commit: Whether to commit the transaction.
            
        Returns:
            Entity: The created entity with identity and audit fields.
        """
        ...
    
    async def update(
        self,
        id: str,
        entity: EntityData,
        updated_by: str,
        commit: bool = True,
    ) -> Entity | None:
        """Update an entity.
        
        Args:
            id: Unique identifier of the entity to update.
            entity: Business data to update.
            updated_by: User identifier for audit trail.
            commit: Whether to commit the transaction.
            
        Returns:
            Entity | None: The updated entity if found, None otherwise.
        """
        ...
    
    async def delete(
        self,
        id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Delete an entity (soft delete).
        
        Args:
            id: Unique identifier of the entity to delete.
            deleted_by: User identifier for audit trail.
            commit: Whether to commit the transaction.
            
        Returns:
            bool: True if deleted, False if not found.
        """
        ...
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        ...
    
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        ...
```

### Interface with Domain-Specific Methods

```python
"""Prompt ownership repository interface."""

from typing import Protocol

from ..entities import PromptOwnership, PromptOwnershipData
from ..enums import AccessLevel, OwnerType


class PromptOwnershipRepositoryInterface(Protocol):
    """Prompt ownership repository interface.
    
    Defines contract for persistence operations on prompt ownership records.
    Supports polymorphic ownership and access control.
    """
    
    # Standard CRUD methods...
    
    async def find_by_prompt_id(self, prompt_id: str) -> list[PromptOwnership]:
        """Find all ownership records for a specific prompt.
        
        Args:
            prompt_id: Unique identifier of the prompt.
            
        Returns:
            list[PromptOwnership]: All ownership records for the prompt.
        """
        ...
    
    async def find_by_owner(
        self, owner_type: OwnerType, owner_id: str
    ) -> list[PromptOwnership]:
        """Find all ownership records for a specific owner.
        
        Args:
            owner_type: Type of owner entity.
            owner_id: Identifier of the owner.
            
        Returns:
            list[PromptOwnership]: All ownership records for the owner.
        """
        ...
    
    async def check_access(
        self,
        prompt_id: str,
        owner_type: OwnerType,
        owner_id: str,
        required_level: AccessLevel,
    ) -> bool:
        """Check if owner has required access level to prompt.
        
        Args:
            prompt_id: Unique identifier of the prompt.
            owner_type: Type of owner entity.
            owner_id: Identifier of the owner.
            required_level: Minimum required access level.
            
        Returns:
            bool: True if owner has required access or higher.
        """
        ...
    
    async def revoke_access(
        self,
        prompt_id: str,
        owner_type: OwnerType,
        owner_id: str,
        deleted_by: str,
        commit: bool = True,
    ) -> bool:
        """Revoke access for a specific owner to a prompt.
        
        Args:
            prompt_id: Unique identifier of the prompt.
            owner_type: Type of owner entity.
            owner_id: Identifier of the owner.
            deleted_by: User identifier for audit trail.
            commit: Whether to commit the transaction.
            
        Returns:
            bool: True if access was revoked, False if not found.
        """
        ...
```

### Package Structure (`__init__.py`)

```python
"""[Domain] domain interfaces package."""

from .entity_repository import EntityRepositoryInterface
from .other_repository import OtherRepositoryInterface


__all__ = [
    "EntityRepositoryInterface",
    "OtherRepositoryInterface",
]
```

## Implementation Guidelines

### Repository Implementation Structure

```
repositories/
├── __init__.py
└── prompt/
    ├── __init__.py
    ├── mysql.py          # MySQL-specific implementation
    ├── sqlite.py         # SQLite-specific implementation
    └── common/
        ├── __init__.py
        └── sql.py        # Common SQL implementation
```

### Common SQL Implementation

The base implementation for all SQL databases:

```python
"""Common SQL repository implementation for Entity."""

from typing import Any
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domains.xxx.domain.entities import Entity, EntityData
from app.domains.xxx.models import EntityModel


class SQLEntityRepository:
    """Common SQL implementation for Entity repository.
    
    This repository provides async CRUD operations using SQLAlchemy/SQLModel.
    It handles conversion between ORM models and domain entities.
    
    Database-specific implementations inherit from this class.
    
    Responsibilities:
    - Execute async database queries
    - Convert ORM models to domain entities
    - Handle transactions
    - Return None when entities are not found (not exceptions)
    
    Note: Business exceptions should be handled in the Service layer.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with an async database session.
        
        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self.session = session
    
    # Implementation of interface methods...
```

### Database-Specific Implementation

```python
"""MySQL-specific implementation for Entity repository."""

from .common import SQLEntityRepository


class MySQLEntityRepository(SQLEntityRepository):
    """MySQL implementation of Entity repository.
    
    Inherits all CRUD operations from SQLEntityRepository.
    Override methods here only when MySQL-specific functionality is needed:
    - MySQL-specific JSON operators
    - Full-text search
    - MySQL-specific optimizations
    """
    
    # Add MySQL-specific methods or overrides here if needed
    pass
```

## Best Practices

### ✅ DO

1. **Use Protocol for structural subtyping**
   ```python
   from typing import Protocol
   
   class EntityRepositoryInterface(Protocol):  # ✅
   ```

2. **Return None for not found (don't raise exceptions)**
   ```python
   async def get_by_id(self, id: str) -> Entity | None:  # ✅
       """Returns None if not found."""
   ```

3. **Return empty list for no results**
   ```python
   async def find(self, filters: dict[str, Any]) -> list[Entity]:  # ✅
       """Returns empty list if none found."""
   ```

4. **Use EntityData for create/update operations**
   ```python
   async def create(self, entity: EntityData, ...) -> Entity:  # ✅
   ```

5. **Include audit parameters**
   ```python
   async def create(self, entity: EntityData, created_by: str, ...) -> Entity:  # ✅
   ```

6. **Support optional commit for transaction control**
   ```python
   async def create(..., commit: bool = True) -> Entity:  # ✅
   ```

7. **Use async/await for all methods**
   ```python
   async def get_by_id(self, id: str) -> Entity | None:  # ✅
   ```

8. **Document return values for not found cases**
   ```python
   """Returns:
       Entity | None: The entity if found, None otherwise.
   """
   ```

### ❌ DON'T

1. **Don't raise exceptions in interfaces**
   ```python
   async def get_by_id(self, id: str) -> Entity:  # ❌
       """Raises: EntityNotFoundException"""  # Wrong layer!
   ```

2. **Don't use ABC instead of Protocol**
   ```python
   from abc import ABC, abstractmethod
   
   class EntityRepositoryInterface(ABC):  # ❌ Use Protocol
   ```

3. **Don't return ORM models**
   ```python
   async def get_by_id(self, id: str) -> EntityModel:  # ❌
       # Should return Entity (domain entity), not EntityModel (ORM)
   ```

4. **Don't mix business logic in interface**
   ```python
   async def create_and_notify(self, ...) -> Entity:  # ❌
       # Interfaces are for persistence only
   ```

5. **Don't forget transaction methods**
   ```python
   class EntityRepositoryInterface(Protocol):
       # ... CRUD methods ...
       # ❌ Missing commit() and rollback()
   ```

6. **Don't use synchronous methods**
   ```python
   def get_by_id(self, id: str) -> Entity | None:  # ❌ Missing async
   ```

7. **Don't forget type hints**
   ```python
   async def find(self, filters) -> list:  # ❌ Missing type hints
   ```

8. **Don't forget docstrings**
   ```python
   async def get_by_id(self, id: str) -> Entity | None:  # ❌ No docstring
       ...
   ```

## Error Handling Strategy

### Repository Layer (Interface Implementation)

**Repositories should:**
- Return `None` when entity not found
- Return empty `list[]` when no results
- Return `False` when operation fails
- Raise infrastructure exceptions (database errors, connection issues)

```python
# ✅ Repository implementation
async def get_by_id(self, id: str) -> Prompt | None:
    result = await self.session.execute(select(PromptModel).where(...))
    model = result.scalar_one_or_none()
    if not model:
        return None  # ✅ Return None, don't raise
    return Prompt.model_validate(model)
```

### Service Layer

**Services should:**
- Check for `None` and raise domain exceptions
- Handle business logic validation
- Coordinate multiple repository calls

```python
# ✅ Service layer
async def get_prompt(self, prompt_id: str) -> Prompt:
    prompt = await self.repository.get_by_id(prompt_id)
    if not prompt:
        raise PromptNotFoundException(prompt_id)  # ✅ Service raises
    return prompt
```

## Transaction Patterns

### Pattern 1: Auto-Commit (Default)

```python
# Create with automatic commit
prompt = await repository.create(
    entity=prompt_data,
    created_by="user123",
    commit=True,  # Default
)
```

### Pattern 2: Manual Transaction

```python
try:
    # Multiple operations in single transaction
    prompt = await repository.create(
        entity=prompt_data,
        created_by="user123",
        commit=False,  # Don't commit yet
    )
    
    ownership = await ownership_repository.create(
        entity=ownership_data,
        created_by="user123",
        commit=False,  # Don't commit yet
    )
    
    # Commit all changes
    await repository.commit()
    await ownership_repository.commit()
    
except Exception:
    # Rollback on error
    await repository.rollback()
    await ownership_repository.rollback()
    raise
```

### Pattern 3: Service-Level Transaction

```python
async def create_prompt_with_ownership(
    self,
    prompt_data: PromptData,
    ownership_data: PromptOwnershipData,
    user_id: str,
) -> tuple[Prompt, PromptOwnership]:
    """Create prompt and ownership in single transaction."""
    try:
        prompt = await self.prompt_repository.create(
            entity=prompt_data,
            created_by=user_id,
            commit=False,
        )
        
        ownership_data.prompt_id = prompt.id
        ownership = await self.ownership_repository.create(
            entity=ownership_data,
            created_by=user_id,
            commit=False,
        )
        
        await self.prompt_repository.commit()
        await self.ownership_repository.commit()
        
        return prompt, ownership
        
    except Exception:
        await self.prompt_repository.rollback()
        await self.ownership_repository.rollback()
        raise
```

## Checklist

- [ ] Interface uses `Protocol` from `typing`
- [ ] Filename is `{entity}_repository.py`
- [ ] Class name is `{Entity}RepositoryInterface`
- [ ] All methods are `async`
- [ ] All methods have complete docstrings
- [ ] All methods have type hints
- [ ] Methods use `...` as body (not `pass`)
- [ ] Query methods return `Entity | None` or `list[Entity]`
- [ ] Create method returns `Entity` (not None)
- [ ] Update/Delete methods handle not found properly
- [ ] Audit parameters included (`created_by`, `updated_by`, `deleted_by`)
- [ ] Transaction methods at the end (`commit`, `rollback`)
- [ ] `commit` parameter defaults to `True`
- [ ] Interface exported in `__init__.py`
- [ ] No business logic in interface
- [ ] No infrastructure coupling (no ORM imports)

## Common Patterns

### Pattern 1: Basic CRUD Repository

For simple entities with standard CRUD operations.

```python
class EntityRepositoryInterface(Protocol):
    async def find(...) -> list[Entity]: ...
    async def count(...) -> int: ...
    async def get_by_id(...) -> Entity | None: ...
    async def create(...) -> Entity: ...
    async def update(...) -> Entity | None: ...
    async def delete(...) -> bool: ...
    async def commit() -> None: ...
    async def rollback() -> None: ...
```

### Pattern 2: Relationship Repository

For entities with complex relationships.

```python
class OwnershipRepositoryInterface(Protocol):
    # Standard CRUD
    async def get_by_id(...) -> Ownership | None: ...
    async def create(...) -> Ownership: ...
    
    # Relationship queries
    async def find_by_prompt_id(...) -> list[Ownership]: ...
    async def find_by_owner(...) -> list[Ownership]: ...
    
    # Business operations
    async def check_access(...) -> bool: ...
    async def revoke_access(...) -> bool: ...
    
    # Transactions
    async def commit() -> None: ...
    async def rollback() -> None: ...
```

### Pattern 3: Read-Only Repository

For entities that are not modified (e.g., history, logs).

```python
class HistoryRepositoryInterface(Protocol):
    # Query methods only
    async def find(...) -> list[History]: ...
    async def count(...) -> int: ...
    async def get_by_id(...) -> History | None: ...
    
    # Create only (no update/delete)
    async def create(...) -> History: ...
    
    # Admin only
    async def hard_delete(...) -> bool: ...
    
    # Transactions
    async def commit() -> None: ...
    async def rollback() -> None: ...
```

## When to Create Repository Interfaces

✅ **Create Repository Interface When:**
- Entity requires persistence
- Need to abstract database operations
- Want to support multiple database implementations
- Testing requires mock repositories
- Following DDD and Clean Architecture

❌ **Don't Create Repository Interface When:**
- Entity is a pure value object (no identity)
- Data is in-memory only
- External API is the data source (use API client instead)
- Read-only configuration data (use config reader)

## Testing Interfaces

### Mock Repository for Testing

```python
class MockPromptRepository:
    """Mock implementation for testing."""
    
    def __init__(self) -> None:
        self._storage: dict[str, Prompt] = {}
    
    async def get_by_id(self, id: str) -> Prompt | None:
        return self._storage.get(id)
    
    async def create(
        self,
        entity: PromptData,
        created_by: str,
        commit: bool = True,
    ) -> Prompt:
        prompt = Prompt(
            id=str(ULID()),
            **entity.model_dump(),
            created_by=created_by,
            updated_by=created_by,
        )
        self._storage[prompt.id] = prompt
        return prompt
    
    async def commit(self) -> None:
        pass
    
    async def rollback(self) -> None:
        self._storage.clear()
```

### Using Mock in Tests

```python
async def test_create_prompt():
    """Test prompt creation service."""
    mock_repo = MockPromptRepository()
    service = PromptService(repository=mock_repo)
    
    prompt_data = PromptData(name="Test Prompt")
    prompt = await service.create_prompt(prompt_data, user_id="user123")
    
    assert prompt.name == "Test Prompt"
    assert prompt.created_by == "user123"
```

## References

- **Entities.md**: For domain entities used in interfaces
- **Value_Objects.md**: For value objects used as parameters
- **Exceptions.md**: For exception handling in services
- **Repository Pattern**: Martin Fowler's Patterns of Enterprise Application Architecture
- **Clean Architecture**: Robert C. Martin (Uncle Bob)
- **DDD**: Eric Evans - Domain-Driven Design

